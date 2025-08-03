from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, ActiveModel


class ContactMessage(TimeStampedModel):
    """Сообщение из контактной формы"""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    message = models.TextField(verbose_name=_('Message'))
    
    is_read = models.BooleanField(default=False, verbose_name=_('Is Read'))
    read_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Read At'))
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('replied', _('Replied')),
        ('closed', _('Closed')),
        ('spam', _('Spam')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name=_('Status'))

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"


class ContactResponse(TimeStampedModel):
    """Ответ на сообщение из контактной формы"""
    contact_message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE, related_name='responses', verbose_name=_('Contact Message'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    message = models.TextField(verbose_name=_('Message'))
    
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Sent At'))
    is_sent = models.BooleanField(default=False, verbose_name=_('Is Sent'))
    
    error_message = models.TextField(blank=True, verbose_name=_('Error Message'))

    class Meta:
        verbose_name = _('Contact Response')
        verbose_name_plural = _('Contact Responses')
        ordering = ['-created_at']

    def __str__(self):
        return f"Response to {self.contact_message.name}: {self.subject}"


class Newsletter(TimeStampedModel, ActiveModel):
    """Рассылка новостей"""
    subject_en = models.CharField(max_length=200, verbose_name=_('Subject (EN)'))
    subject_ru = models.CharField(max_length=200, blank=True, verbose_name=_('Subject (RU)'))
    subject_he = models.CharField(max_length=200, blank=True, verbose_name=_('Subject (HE)'))
    
    content_en = models.TextField(verbose_name=_('Content (EN)'))
    content_ru = models.TextField(blank=True, verbose_name=_('Content (RU)'))
    content_he = models.TextField(blank=True, verbose_name=_('Content (HE)'))
    
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Sent At'))
    is_sent = models.BooleanField(default=False, verbose_name=_('Is Sent'))
    
    recipients_count = models.PositiveIntegerField(default=0, verbose_name=_('Recipients Count'))
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('scheduled', _('Scheduled')),
        ('sending', _('Sending')),
        ('sent', _('Sent')),
        ('failed', _('Failed')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name=_('Status'))
    
    scheduled_for = models.DateTimeField(blank=True, null=True, verbose_name=_('Scheduled For'))

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-created_at']

    def __str__(self):
        return self.subject_en