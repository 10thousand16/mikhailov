from django.urls import path
from . import views

app_name = 'stolovaya'

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('category/<slug:slug>/', views.dish_list_by_category, name='dish_list_by_category'),
    path('dish/<slug:slug>/', views.dish_detail, name='dish_detail'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/count/', views.cart_count, name='cart_count'),                     # новый
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),  # новый
    path('order/create/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('dish/create/', views.dish_create, name='dish_create'),
    path('dish/edit/<slug:slug>/', views.dish_edit, name='dish_edit'),
    path('dish/delete/<slug:slug>/', views.dish_delete, name='dish_delete'),
]