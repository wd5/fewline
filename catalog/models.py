          # -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from django.core.exceptions import ValidationError

class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    SEO_text = models.TextField(null=True, blank=True)
    sort_number = models.IntegerField()
    image = FileBrowseField("Image", max_length=200, directory="", extensions=[".jpg", ".png"], blank=True, null=True)

    class Meta:
        ordering = ['sort_number']
        verbose_name_plural = 'Секции товара'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('section-page', [str(self.slug)])

class CategoryProduct(models.Model):
    category = models.ForeignKey('Category')
    product = models.ForeignKey('Product', verbose_name='Товар')
    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        ordering = ['position']

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    section = models.ForeignKey(Section)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    SEO_text = models.TextField(null=True, blank=True)
    image = FileBrowseField("Image", max_length=200, directory="", extensions=[".jpg", ".png"], blank=True, null=True)
    description = models.TextField()
    meta_keywords = models.TextField(blank=True)
    meta_descriotion = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField("Position")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Категории товара'

    @models.permalink
    def get_absolute_url(self):
        return ('catalog-page', [str(self.slug)])

def validate_even(value):
        if len(value) > 500:
            raise ValidationError(u'Количество символов: %s. Максимально разрешенное: 500'% len(value) )


class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Категория', through=CategoryProduct)
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name='Цена')
    wholesale_price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name='Цена закупки')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    mini_html_description = models.TextField(help_text='Максимальное количество символов: 140.',
                                        verbose_name='Мини описание в HTML')
    html_description = models.TextField(blank=True, verbose_name='Описание', help_text='Описание в HTML')
    tech_details = models.TextField(blank=True)
    thumbnail_image = FileBrowseField("Image", max_length=200, directory="products_image/videocamers", extensions=[".jpg", ".jpeg", ".png"], blank=True, null=True)
    # Метаданные товара
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_discount = models.BooleanField(default=True, verbose_name='Скидка')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    # Временные отметки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product-page', [str(self.slug)])

    class Meta:
        verbose_name_plural = 'Товар'

class ProductPhoto(models.Model):
    item = models.ForeignKey(Product)
    image = FileBrowseField("Image", max_length=200, directory="products_image", extensions=[".jpg", ".jpeg", ".png"], blank=True, null=True)

    class Meta:
        ordering = ['item']
        verbose_name_plural = 'Фото товара'

    def __unicode__(self):
        return self.image.url

    @models.permalink
    def get_absolute_url(self):
        return ('item_detail', None, {'object_id': self.id})

class File(models.Model):
    product = models.ForeignKey(Product, verbose_name='Файл')
    name = models.CharField(max_length=100, verbose_name='Название')
    file = FileBrowseField(max_length=100, directory="files", blank=True, null=True)

    def __unicode__(self):
        return self.name
