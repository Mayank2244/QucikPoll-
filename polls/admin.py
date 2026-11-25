
from django.contrib import admin

from .models import Poll, Option, Vote


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "status", "closes_at", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "creator__username")
    inlines = [OptionInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "option", "user", "created_at")
    list_filter = ("poll",)
    search_fields = ("user__username", "poll__title")
