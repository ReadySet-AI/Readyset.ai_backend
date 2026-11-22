from django.contrib import admin
from django.contrib.auth.models import Group

from users.services.email import send_invitation_email
from users.models import CustomUser, Roles


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    list_filter = ('id', 'email')
    exclude = (
        'password',
        'date_joined',
        'groups',
        'user_permissions',
        'last_login',
        'is_superuser',
        'is_staff',
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            if (
                not change
                and obj.role
                in [
                    Roles.Mentor.name,
                    Roles.Global_Admin.name,
                    Roles.Company_Admin.name,
                ]
                and not obj.is_active
            ):
                send_invitation_email(obj)
        except Exception as e:
            self.message_user(
                request,
                f"Error sending invitation email: {str(e)}",
                level="error",
            )


admin.site.unregister(Group)
