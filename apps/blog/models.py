from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.core.models import (
    TimeStampedModel, 
    SEOModel, 
    SlugModel, 
    ActiveModel, 
    PublishableModel, 
    ViewableModel, 
    FeaturedModel,
    get_image_upload_path
)


class Category(TimeStampedModel, SlugModel, ActiveModel):
    """Категория блога"""
    name_en = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Name (RU)'))
    name_he = models.CharField(max_length=100, blank=True, verbose_name=_('Name (HE)'))
    
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    icon = models.CharField(max_length=50, blank=True, verbose_name=_('Icon'))
    color = models.CharField(max_length=20, blank=True, verbose_name=_('Color'))
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('Parent Category'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order']

    def __str__(self):
        return self.name_en


class Tag(TimeStampedModel, SlugModel, ActiveModel):
    """Тег для статей блога"""
    name_en = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Name (RU)'))
    name_he = models.CharField(max_length=100, blank=True, verbose_name=_('Name (HE)'))
    
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    color = models.CharField(max_length=20, blank=True, verbose_name=_('Color'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name_en']

    def __str__(self):
        return self.name_en


class Post(TimeStampedModel, SlugModel, SEOModel, PublishableModel, ViewableModel, FeaturedModel):
    """Статья блога"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('Author'))
    
    title_en = models.CharField(max_length=200, verbose_name=_('Title (EN)'))
    title_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Title (RU)'))
    title_he = models.CharField(max_length=200, blank=True, verbose_name=_('Title (HE)'))
    
    subtitle_en = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (EN)'))
    subtitle_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (RU)'))
    subtitle_he = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (HE)'))
    
    excerpt_en = models.TextField(blank=True, verbose_name=_('Excerpt (EN)'))
    excerpt_ru = models.TextField(blank=True, verbose_name=_('Excerpt (RU)'))
    excerpt_he = models.TextField(blank=True, verbose_name=_('Excerpt (HE)'))
    
    content_en = models.TextField(verbose_name=_('Content (EN)'))
    content_ru = models.TextField(blank=True, verbose_name=_('Content (RU)'))
    content_he = models.TextField(blank=True, verbose_name=_('Content (HE)'))
    
    thumbnail = models.ImageField(upload_to=get_image_upload_path, verbose_name=_('Thumbnail'))
    cover_image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, verbose_name=_('Cover Image'))
    
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name=_('Categories'))
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name=_('Tags'))
    
    read_time = models.PositiveIntegerField(default=0, verbose_name=_('Read Time (minutes)'))
    allow_comments = models.BooleanField(default=True, verbose_name=_('Allow Comments'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Comment(TimeStampedModel, ActiveModel):
    """Комментарий к статье"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'))
    author_name = models.CharField(max_length=100, verbose_name=_('Author Name'))
    author_email = models.EmailField(verbose_name=_('Author Email'))
    author_website = models.URLField(blank=True, verbose_name=_('Author Website'))
    
    content = models.TextField(verbose_name=_('Content'))
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies', verbose_name=_('Parent Comment'))
    
    is_approved = models.BooleanField(default=False, verbose_name=_('Is Approved'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title_en}"


class Subscription(TimeStampedModel):
    """Подписка на блог"""
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    name = models.CharField(max_length=100, blank=True, verbose_name=_('Name'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Confirmed At'))
    
    language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('ru', 'Русский'),
        ('he', 'עברית')
    ], verbose_name=_('Language'))
    
    token = models.CharField(max_length=100, blank=True, verbose_name=_('Confirmation Token'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['-created_at']

    def __str__(self):
        return self.email