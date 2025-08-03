from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class PageView(TimeStampedModel):
    """Просмотр страницы"""
    path = models.CharField(max_length=255, default='/', verbose_name=_('Path'))
    query_params = models.JSONField(blank=True, null=True, verbose_name=_('Query Parameters'))
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    
    referrer = models.URLField(blank=True, verbose_name=_('Referrer'))
    language = models.CharField(max_length=10, blank=True, verbose_name=_('Language'))
    
    session_id = models.CharField(max_length=100, blank=True, verbose_name=_('Session ID'))
    visitor_id = models.CharField(max_length=100, blank=True, verbose_name=_('Visitor ID'))
    
    duration = models.PositiveIntegerField(default=0, verbose_name=_('Duration (seconds)'))
    
    is_bot = models.BooleanField(default=False, verbose_name=_('Is Bot'))
    is_mobile = models.BooleanField(default=False, verbose_name=_('Is Mobile'))
    
    country = models.CharField(max_length=100, blank=True, verbose_name=_('Country'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))

    class Meta:
        verbose_name = _('Page View')
        verbose_name_plural = _('Page Views')
        ordering = ['-created_at']

    def __str__(self):
        return f"View of {self.path} at {self.created_at}"


class Event(TimeStampedModel):
    """Событие на сайте"""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('Category'))
    
    data = models.JSONField(blank=True, null=True, verbose_name=_('Data'))
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    
    session_id = models.CharField(max_length=100, blank=True, verbose_name=_('Session ID'))
    visitor_id = models.CharField(max_length=100, blank=True, verbose_name=_('Visitor ID'))
    
    path = models.CharField(max_length=255, blank=True, verbose_name=_('Path'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.category}) at {self.created_at}"


class Visitor(TimeStampedModel):
    """Посетитель сайта"""
    visitor_id = models.CharField(max_length=100, unique=True, verbose_name=_('Visitor ID'))
    
    first_visit_at = models.DateTimeField(auto_now_add=True, verbose_name=_('First Visit At'))
    last_visit_at = models.DateTimeField(auto_now=True, verbose_name=_('Last Visit At'))
    
    visits_count = models.PositiveIntegerField(default=1, verbose_name=_('Visits Count'))
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    
    browser = models.CharField(max_length=100, blank=True, verbose_name=_('Browser'))
    os = models.CharField(max_length=100, blank=True, verbose_name=_('Operating System'))
    device = models.CharField(max_length=100, blank=True, verbose_name=_('Device'))
    
    country = models.CharField(max_length=100, blank=True, verbose_name=_('Country'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    
    language = models.CharField(max_length=10, blank=True, verbose_name=_('Language'))
    
    referrer = models.URLField(blank=True, verbose_name=_('First Referrer'))
    
    is_bot = models.BooleanField(default=False, verbose_name=_('Is Bot'))

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
        ordering = ['-last_visit_at']

    def __str__(self):
        return f"Visitor {self.visitor_id} ({self.visits_count} visits)"


class VisitorSession(TimeStampedModel):
    """Сессия посетителя"""
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Visitor'))
    session_id = models.CharField(max_length=100, unique=True, verbose_name=_('Session ID'))
    
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Start Time'))
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_('End Time'))
    
    duration = models.PositiveIntegerField(default=0, verbose_name=_('Duration (seconds)'))
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    
    entry_page = models.CharField(max_length=255, blank=True, verbose_name=_('Entry Page'))
    exit_page = models.CharField(max_length=255, blank=True, verbose_name=_('Exit Page'))
    
    pages_viewed = models.PositiveIntegerField(default=0, verbose_name=_('Pages Viewed'))
    
    referrer = models.URLField(blank=True, verbose_name=_('Referrer'))
    
    is_bounce = models.BooleanField(default=True, verbose_name=_('Is Bounce'))

    class Meta:
        verbose_name = _('Visitor Session')
        verbose_name_plural = _('Visitor Sessions')
        ordering = ['-start_time']

    def __str__(self):
        return f"Session {self.session_id} for {self.visitor}"


class DailyStatistics(models.Model):
    """Ежедневная статистика"""
    date = models.DateField(unique=True, verbose_name=_('Date'))
    
    page_views = models.PositiveIntegerField(default=0, verbose_name=_('Page Views'))
    unique_visitors = models.PositiveIntegerField(default=0, verbose_name=_('Unique Visitors'))
    new_visitors = models.PositiveIntegerField(default=0, verbose_name=_('New Visitors'))
    
    avg_session_duration = models.PositiveIntegerField(default=0, verbose_name=_('Average Session Duration (seconds)'))
    bounce_rate = models.FloatField(default=0.0, verbose_name=_('Bounce Rate'))
    
    top_pages = models.JSONField(blank=True, null=True, verbose_name=_('Top Pages'))
    top_referrers = models.JSONField(blank=True, null=True, verbose_name=_('Top Referrers'))
    
    devices = models.JSONField(blank=True, null=True, verbose_name=_('Devices'))
    browsers = models.JSONField(blank=True, null=True, verbose_name=_('Browsers'))
    countries = models.JSONField(blank=True, null=True, verbose_name=_('Countries'))

    class Meta:
        verbose_name = _('Daily Statistics')
        verbose_name_plural = _('Daily Statistics')
        ordering = ['-date']

    def __str__(self):
        return f"Statistics for {self.date}"