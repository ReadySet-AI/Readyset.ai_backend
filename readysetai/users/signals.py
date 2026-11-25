from django.db.models.signals import post_save
from django.dispatch import receiver
from users.services.email import send_invitation_email
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_activation_email_signal(
    sender, instance, created: bool, **kwargs
) -> None:
    if created:
        send_invitation_email(instance)
