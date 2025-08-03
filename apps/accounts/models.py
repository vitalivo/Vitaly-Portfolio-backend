from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, get_image_upload_path


class UserProfile(TimeStampedModel):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    
    # Персональная информация
    bio_en = models.TextField(blank=True, verbose_name=_('Bio (EN)'))
    bio_ru = models.TextField(blank=True, verbose_name=_('Bio (RU)'))
    bio_he = models.TextField(blank=True, verbose_name=_('Bio (HE)'))
    
    location = models.CharField(max_length=100, blank=True, verbose_name=_('Location'))
    timezone = models.CharField(max_length=50, default='UTC', verbose_name=_('Timezone'))
    language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('ru', 'Русский'),
        ('he', 'עברית')
    ], verbose_name=_('Language'))
    
    avatar = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, verbose_name=_('Avatar'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Phone'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    
    # Профессиональная информация
    job_title_en = models.CharField(max_length=100, blank=True, verbose_name=_('Job Title (EN)'))
    job_title_ru = models.CharField(max_length=100, blank=True, verbose_name=_('Job Title (RU)'))
    job_title_he = models.CharField(max_length=100, blank=True, verbose_name=_('Job Title (HE)'))
    
    company = models.CharField(max_length=100, blank=True, verbose_name=_('Company'))
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name=_('Years of Experience'))
    
    # Социальные сети
    linkedin_url = models.URLField(blank=True, verbose_name=_('LinkedIn URL'))
    github_url = models.URLField(blank=True, verbose_name=_('GitHub URL'))
    telegram_url = models.URLField(blank=True, verbose_name=_('Telegram URL'))
    twitter_url = models.URLField(blank=True, verbose_name=_('Twitter URL'))
    instagram_url = models.URLField(blank=True, verbose_name=_('Instagram URL'))
    
    # Настройки
    is_available_for_hire = models.BooleanField(default=True, verbose_name=_('Available for Hire'))
    show_email_publicly = models.BooleanField(default=False, verbose_name=_('Show Email Publicly'))
    receive_notifications = models.BooleanField(default=True, verbose_name=_('Receive Notifications'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_bio(self, language='en'):
        """Получить биографию на указанном языке"""
        return getattr(self, f'bio_{language}', self.bio_en)

    def get_job_title(self, language='en'):
        """Получить должность на указанном языке"""
        return getattr(self, f'job_title_{language}', self.job_title_en)