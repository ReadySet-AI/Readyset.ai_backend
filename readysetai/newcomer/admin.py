from django.contrib import admin

from newcomer.models import Newcomer


@admin.register(Newcomer)
class NewcomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'mentor', 'post', 'status', 'start_date')
    search_fields = ('user__username', 'user__email', 'post')
