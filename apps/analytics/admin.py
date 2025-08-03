from django.contrib import admin
from .models import PageView, Event, Visitor, VisitorSession, DailyStatistics

admin.site.register(PageView)
admin.site.register(Event)
admin.site.register(Visitor)
admin.site.register(VisitorSession)
admin.site.register(DailyStatistics)