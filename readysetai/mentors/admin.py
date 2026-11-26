from django.contrib import admin

from mentors.models import Mentor


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'status', 'created_at', 'updated_at')
    search_fields = ('user__email', 'post')
