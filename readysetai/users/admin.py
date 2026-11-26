from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    exclude = (
        'password',
        'date_joined',
        'groups',
        'user_permissions',
        'last_login',
        'is_superuser',
        'is_staff',
    )


admin.site.unregister(Group)
