from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.core.models import (
    TimeStampedModel, 
    SEOModel, 
    SlugModel, 
    OrderableModel,
    ActiveModel, 
    PublishableModel, 
    ViewableModel, 
    FeaturedModel,
    get_image_upload_path
)


class Category(TimeStampedModel, SlugModel, OrderableModel, ActiveModel):
    """Категория проектов"""
    name_en = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Name (RU)'))
    name_he = models.CharField(max_length=100, blank=True, verbose_name=_('Name (HE)'))
    
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    icon = models.CharField(max_length=50, blank=True, verbose_name=_('Icon'))
    color = models.CharField(max_length=20, blank=True, verbose_name=_('Color'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['position']

    def __str__(self):
        return self.name_en


class Technology(TimeStampedModel, SlugModel, OrderableModel, ActiveModel):
    """Технология, используемая в проектах"""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    icon = models.CharField(max_length=50, blank=True, verbose_name=_('Icon'))
    logo = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, verbose_name=_('Logo'))
    color = models.CharField(max_length=20, blank=True, verbose_name=_('Color'))
    
    website = models.URLField(blank=True, verbose_name=_('Website'))
    version = models.CharField(max_length=20, blank=True, verbose_name=_('Version'))

    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')
        ordering = ['position']

    def __str__(self):
        return self.name


class Project(TimeStampedModel, SlugModel, SEOModel, PublishableModel, ViewableModel, FeaturedModel):
    """Проект в портфолио"""
    title_en = models.CharField(max_length=200, verbose_name=_('Title (EN)'))
    title_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Title (RU)'))
    title_he = models.CharField(max_length=200, blank=True, verbose_name=_('Title (HE)'))
    
    subtitle_en = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (EN)'))
    subtitle_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (RU)'))
    subtitle_he = models.CharField(max_length=200, blank=True, verbose_name=_('Subtitle (HE)'))
    
    description_en = models.TextField(verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    content_en = models.TextField(blank=True, verbose_name=_('Content (EN)'))
    content_ru = models.TextField(blank=True, verbose_name=_('Content (RU)'))
    content_he = models.TextField(blank=True, verbose_name=_('Content (HE)'))
    
    thumbnail = models.ImageField(upload_to=get_image_upload_path, verbose_name=_('Thumbnail'))
    cover_image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, verbose_name=_('Cover Image'))
    
    categories = models.ManyToManyField(Category, related_name='projects', verbose_name=_('Categories'))
    technologies = models.ManyToManyField(Technology, related_name='projects', verbose_name=_('Technologies'))
    
    client_name = models.CharField(max_length=100, blank=True, verbose_name=_('Client Name'))
    client_website = models.URLField(blank=True, verbose_name=_('Client Website'))
    
    project_url = models.URLField(blank=True, verbose_name=_('Project URL'))
    github_url = models.URLField(blank=True, verbose_name=_('GitHub URL'))
    
    start_date = models.DateField(blank=True, null=True, verbose_name=_('Start Date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('End Date'))
    
    is_ongoing = models.BooleanField(default=False, verbose_name=_('Is Ongoing'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-published_at', 'order']

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Skill(TimeStampedModel, SlugModel, OrderableModel, ActiveModel):
    """Навык или умение"""
    name_en = models.CharField(max_length=100, verbose_name=_('Name (EN)'))
    name_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Name (RU)'))
    name_he = models.CharField(max_length=100, blank=True, verbose_name=_('Name (HE)'))
    
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_ru = models.TextField(blank=True, verbose_name=_('Description (RU)'))
    description_he = models.TextField(blank=True, verbose_name=_('Description (HE)'))
    
    icon = models.CharField(max_length=50, blank=True, verbose_name=_('Icon'))
    level = models.PositiveSmallIntegerField(default=0, choices=[(i, f"{i}%") for i in range(0, 101, 10)], verbose_name=_('Level'))
    
    category = models.CharField(max_length=50, choices=[
        ('frontend', _('Frontend')),
        ('backend', _('Backend')),
        ('database', _('Database')),
        ('devops', _('DevOps')),
        ('design', _('Design')),
        ('soft', _('Soft Skills')),
        ('other', _('Other')),
    ], default='other', verbose_name=_('Category'))
    
    years_experience = models.PositiveSmallIntegerField(default=0, verbose_name=_('Years of Experience'))

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'position']

    def __str__(self):
        return self.name_en