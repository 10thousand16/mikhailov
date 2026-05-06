from django.contrib import admin
from .models import Category, Dish, Order, OrderItem

class DishInline(admin.TabularInline):
    model = Dish
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DishInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['dish']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created']
    list_filter = ['category', 'available', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'total_price', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['full_name', 'phone', 'email']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'quantity', 'price']