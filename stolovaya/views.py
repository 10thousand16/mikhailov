from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Dish, Order, OrderItem, Category
from .forms import DishForm, OrderForm
from .cart import Cart

def dish_list(request):
    dishes = Dish.objects.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'stolovaya/dish_list.html', {'dishes': dishes, 'categories': categories})

def dish_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    dishes = Dish.objects.filter(category=category, available=True)
    categories = Category.objects.all()
    return render(request, 'stolovaya/dish_list.html', {'dishes': dishes, 'categories': categories, 'selected_category': category})

def dish_detail(request, slug):
    dish = get_object_or_404(Dish, slug=slug, available=True)
    return render(request, 'stolovaya/dish_detail.html', {'dish': dish})

def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart(request)
    cart.add(dish, quantity=1)
    messages.success(request, f'"{dish.name}" добавлено в корзину')
    return redirect('stolovaya:dish_list')

def remove_from_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart(request)
    cart.remove(dish)
    messages.info(request, f'"{dish.name}" удалено из корзины')
    return redirect('stolovaya:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'stolovaya/cart.html', {'cart': cart})

def create_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Корзина пуста. Добавьте блюда для оформления заказа.')
        return redirect('stolovaya:dish_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.session_key = request.session.session_key
                order.total_price = cart.get_total_price()
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        dish=item['dish'],
                        quantity=item['quantity'],
                        price=item['price']
                    )
                cart.clear()
                messages.success(request, f'Заказ №{order.id} успешно оформлен! Мы свяжемся с вами.')
                return redirect('stolovaya:order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'stolovaya/order_form.html', {'form': form, 'cart': cart})

def order_list(request):
    session_key = request.session.session_key
    orders = Order.objects.filter(session_key=session_key).order_by('-created')
    return render(request, 'stolovaya/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, session_key=request.session.session_key)
    return render(request, 'stolovaya/order_detail.html', {'order': order})

# CRUD для блюд (только для персонала)
def staff_check(user):
    return user.is_staff

@user_passes_test(staff_check)
def dish_create(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save()
            messages.success(request, f'Блюдо "{dish.name}" создано')
            return redirect('stolovaya:dish_detail', slug=dish.slug)
    else:
        form = DishForm()
    return render(request, 'stolovaya/dish_form.html', {'form': form, 'title': 'Создать блюдо'})

@user_passes_test(staff_check)
def dish_edit(request, slug):
    dish = get_object_or_404(Dish, slug=slug)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, f'Блюдо "{dish.name}" обновлено')
            return redirect('stolovaya:dish_detail', slug=dish.slug)
    else:
        form = DishForm(instance=dish)
    return render(request, 'stolovaya/dish_form.html', {'form': form, 'title': 'Редактировать блюдо'})

@user_passes_test(staff_check)
def dish_delete(request, slug):
    dish = get_object_or_404(Dish, slug=slug)
    if request.method == 'POST':
        name = dish.name
        dish.delete()
        messages.success(request, f'Блюдо "{name}" удалено')
        return redirect('stolovaya:dish_list')
    return render(request, 'stolovaya/dish_confirm_delete.html', {'dish': dish})

# -------- AJAX-функции для корзины (добавлено в пункте 3) --------
def cart_count(request):
    """Возвращает количество товаров в корзине в формате JSON"""
    cart = Cart(request)
    return JsonResponse({'count': len(cart)})

@require_POST
def add_to_cart_ajax(request):
    """AJAX-обработчик добавления товара в корзину"""
    try:
        data = json.loads(request.body)
        dish_id = data.get('dish_id')
        dish = get_object_or_404(Dish, id=dish_id, available=True)
        cart = Cart(request)
        cart.add(dish, quantity=1)
        return JsonResponse({'status': 'ok', 'message': f'{dish.name} добавлено'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)