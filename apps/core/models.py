from django.db import models
from django.utils.translation import gettext_lazy as _
import os
import uuid


def get_image_upload_path(instance, filename):
    """Генерирует путь для загрузки изображений"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', instance.__class__.__name__.lower(), filename)


class TimeStampedModel(models.Model):
    """Абстрактная модель с временными метками"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Абстрактная модель с SEO полями"""
    meta_title = models.CharField(max_length=60, blank=True, verbose_name=_('Meta Title'))
    meta_description = models.CharField(max_length=160, blank=True, verbose_name=_('Meta Description'))
    meta_keywords = models.TextField(blank=True, verbose_name=_('Meta Keywords'))
    
    class Meta:
        abstract = True


class SlugModel(models.Model):
    """Абстрактная модель со slug полем"""
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))
    
    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Абстрактная модель с полем порядка"""
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
    
    class Meta:
        abstract = True
        ordering = ['order']


class OrderableModel(models.Model):
    """Абстрактная модель с возможностью сортировки"""
    position = models.PositiveIntegerField(default=0, verbose_name=_('Position'))
    
    class Meta:
        abstract = True
        ordering = ['position']


class ActiveModel(models.Model):
    """Абстрактная модель с полем активности"""
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    class Meta:
        abstract = True


class MultiLanguageModel(models.Model):
    """Абстрактная модель для многоязычных полей"""
    class Meta:
        abstract = True
    
    def get_field_value(self, field_name, language='en'):
        """Получить значение поля на указанном языке"""
        localized_field = f"{field_name}_{language}"
        return getattr(self, localized_field, getattr(self, f"{field_name}_en", ''))


class PublishableModel(models.Model):
    """Абстрактная модель для публикуемых объектов"""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name=_('Status')
    )
    published_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Published At'))
    
    class Meta:
        abstract = True

    def is_published(self):
        """Проверить, опубликован ли объект"""
        return self.status == 'published'


class ViewableModel(models.Model):
    """Абстрактная модель для отслеживания просмотров"""
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Views Count'))
    
    class Meta:
        abstract = True

    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class FeaturedModel(models.Model):
    """Абстрактная модель для рекомендуемых объектов"""
    is_featured = models.BooleanField(default=False, verbose_name=_('Is Featured'))
    featured_order = models.PositiveIntegerField(default=0, verbose_name=_('Featured Order'))
    
    class Meta:
        abstract = True


class RatableModel(models.Model):
    """Абстрактная модель для рейтинга"""
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        verbose_name=_('Rating')
    )
    rating_count = models.PositiveIntegerField(default=0, verbose_name=_('Rating Count'))
    
    class Meta:
        abstract = True

    def update_rating(self, new_rating):
        """Обновить рейтинг"""
        total_rating = (self.rating * self.rating_count) + new_rating
        self.rating_count += 1
        self.rating = total_rating / self.rating_count
        self.save(update_fields=['rating', 'rating_count'])


class SiteSettings(TimeStampedModel):
    """Настройки сайта"""
    site_name_en = models.CharField(max_length=100, verbose_name=_('Site Name (EN)'))
    site_name_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Site Name (RU)'))
    site_name_he = models.CharField(max_length=100, blank=True, verbose_name=_('Site Name (HE)'))
    
    tagline_en = models.CharField(max_length=200, blank=True, verbose_name=_('Tagline (EN)'))
    tagline_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Tagline (RU)'))
    tagline_he = models.CharField(max_length=200, blank=True, verbose_name=_('Tagline (HE)'))
    
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name=_('Logo'))
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name=_('Favicon'))
    
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Phone'))
    address_en = models.TextField(blank=True, verbose_name=_('Address (EN)'))
    address_ru = models.TextField(blank=True, verbose_name=_('Address (RU)'))
    address_he = models.TextField(blank=True, verbose_name=_('Address (HE)'))
    
    linkedin_url = models.URLField(blank=True, verbose_name=_('LinkedIn URL'))
    github_url = models.URLField(blank=True, verbose_name=_('GitHub URL'))
    telegram_url = models.URLField(blank=True, verbose_name=_('Telegram URL'))
    
    is_maintenance_mode = models.BooleanField(default=False, verbose_name=_('Maintenance Mode'))
    maintenance_message_en = models.TextField(blank=True, verbose_name=_('Maintenance Message (EN)'))
    maintenance_message_ru = models.TextField(blank=True, verbose_name=_('Maintenance Message (RU)'))
    maintenance_message_he = models.TextField(blank=True, verbose_name=_('Maintenance Message (HE)'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name=_('Google Analytics ID'))
    yandex_metrica_id = models.CharField(max_length=50, blank=True, verbose_name=_('Yandex Metrica ID'))

    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return self.site_name_en or 'Site Settings'


class SEOSettings(TimeStampedModel):
    """SEO настройки для разных страниц"""
    PAGE_TYPES = [
        ('home', _('Home Page')),
        ('about', _('About Page')),
        ('portfolio', _('Portfolio Page')),
        ('blog', _('Blog Page')),
        ('contact', _('Contact Page')),
        ('resume', _('Resume Page')),
    ]

    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True, verbose_name=_('Page Type'))
    
    title_en = models.CharField(max_length=60, verbose_name=_('Title (EN)'))
    title_ru = models.CharField(max_length=60, blank=True, verbose_name=_('Title (RU)'))
    title_he = models.CharField(max_length=60, blank=True, verbose_name=_('Title (HE)'))
    
    description_en = models.CharField(max_length=160, verbose_name=_('Description (EN)'))
    description_ru = models.CharField(max_length=160, blank=True, verbose_name=_('Description (RU)'))
    description_he = models.CharField(max_length=160, blank=True, verbose_name=_('Description (HE)'))
    
    keywords_en = models.TextField(blank=True, verbose_name=_('Keywords (EN)'))
    keywords_ru = models.TextField(blank=True, verbose_name=_('Keywords (RU)'))
    keywords_he = models.TextField(blank=True, verbose_name=_('Keywords (HE)'))
    
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True, verbose_name=_('OG Image'))
    og_type = models.CharField(max_length=20, default='website', verbose_name=_('OG Type'))
    
    schema_markup = models.JSONField(blank=True, null=True, verbose_name=_('Schema Markup'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('SEO Settings')
        verbose_name_plural = _('SEO Settings')
        ordering = ['page_type']

    def __str__(self):
        return f'SEO - {self.get_page_type_display()}'