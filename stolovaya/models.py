from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('stolovaya:dish_list_by_category', args=[self.slug])

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name='Категория', null=True, blank=True)
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='dishes/', blank=True, null=True)
    available = models.BooleanField('Доступно', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stolovaya:dish_detail', args=[self.slug])

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processed', 'Обработан'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменён'),
    )
    session_key = models.CharField('Ключ сессии', max_length=40, blank=True)
    full_name = models.CharField('ФИО', max_length=200)
    address = models.TextField('Адрес доставки')
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    total_price = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f'Заказ #{self.id} от {self.created.strftime("%d.%m.%Y")}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.dish.name} x {self.quantity}'