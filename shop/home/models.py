from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import datetime



class User(AbstractUser):
    SEX_CHOICES = [
        ('м', 'мужской'),
        ('ж', 'женский'),
    ]
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=' ',
        blank=True,
        verbose_name='Пол',
    )
    ROLE_CHOICES = [
        ('u', 'user/пользователь'),
        ('s', 'seller/продавец'),
    ]
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default='u',
        verbose_name='Роль',    
    )
    is_moderated = models.BooleanField(default=False)
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    land = models.CharField(
        max_length=30,
        verbose_name='Страна',
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name='Город',
        blank=True,
        null=True,
    )
    avatat = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse(
            'home:user_account', 
            args=[self.username]
        )


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Название категории',
    )
    slug = models.SlugField(
        max_length=60,
        db_index=True,
        unique=True,
        null=True,
    )

    class Meta:
        ordering=['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'home:product_list_by_category', 
            args=[self.slug]
        )


class Subcategory(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Введите название категории',    
    )
    slug = models.SlugField(
        max_length=60,
        db_index=True,
        unique=True,
        null=True,
    )
    category = models.ForeignKey(
        Category, 
        null=True,
        blank=True,
        verbose_name='Категория',
        help_text='Выберите категорию', 
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering=['name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'home:product_list_by_subcategory', 
            args=[self.slug]
        )


class Brand(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название бренда',
        help_text='Введите название текста',
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        unique=True,
        null=True,
    )
    logo = models.ImageField(
        upload_to='brand_logo/',
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        ordering=['name']
        verbose_name='Бренд'
        verbose_name_plural='Бренды'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'home:product_list_by_brand', 
            args=[self.slug]
        )


class MadeIn(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Страна производства',
        help_text='Введите название страны',
    )
    slug = models.SlugField(
        max_length=50,
        db_index=True,
        unique=True,
        null=True,
    )

    class Meta:
        ordering=['name']
        verbose_name = 'Старана производства'
        verbose_name_plural = 'Страны производства'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
        help_text='Введите название товара',
    )
    slug = models.SlugField(
        max_length=250,
        db_index=True,
        unique=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание товара',
    )
    brand = models.ForeignKey(
        Brand, 
        verbose_name='Бренд', 
        help_text='Выберите бренд товара',
        on_delete=models.CASCADE,
    )
    made_in = models.ForeignKey(
        MadeIn, 
        verbose_name='Сделано в', 
        help_text='Выберите страну производителя',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category, 
        verbose_name='Название категории',
        help_text='Выберите категорию товара', 
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        verbose_name='Название подкатегории',
        help_text='Выберите подкатегорию товара',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        help_text='Введите цену товара',
        max_digits=12, 
        decimal_places=2
    )
    discount_price = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена со скидкой',
        help_text='Введите цену товара со скидкой',
        max_digits=12, 
        decimal_places=2
    )
    discount = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    count = models.IntegerField(
        verbose_name='Количество',
        help_text='Введите количество товара на складе',
    )
    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True,
        verbose_name='Изображение',
        help_text='Добавьте изображение товара',
    )
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'product_detail', 
            args=[self.id, self.slug]
        )


class Comment(models.Model):
    product = models.ForeignKey(
        Product, 
        verbose_name='Товар', 
        help_text='Выберите товар для комментария',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Напишите комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь, написавший комментарий',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return self.text