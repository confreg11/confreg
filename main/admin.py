from django.contrib import admin

# Register your models here.

from .models import UserProfile, Event

admin.site.register(UserProfile)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_date", "created_at")
