from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def generate_uid_token(user):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_invitation_email(user):
    uid, token = generate_uid_token(user)
    subject = "Activate your account"
    message = f"Greetings\n\n Please use the following link to activate your account: {settings.BASE_URL}/activate/{uid}/{token}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
