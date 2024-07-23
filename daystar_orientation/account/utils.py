from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_confirmation_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirmation_link = f"{settings.FRONTEND_URL}/confirm-email/{uid}/{token}/"  # Custom URL

    subject = 'Confirm your email address'
    message = f'Hi {user.name}, please confirm your email address by clicking the link below:\n\n{confirmation_link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
