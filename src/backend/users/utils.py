from random import choices, choice
from string import ascii_letters, digits

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.models import AnonymousUser


User = get_user_model()


def email_exists(email):
    return User.objects.filter(email=email).exists()


def username_exists(username):
    return User.objects.filter(username=username).exists()


def generate_verification_code():
    return ''.join(choices(digits, k=6))


def send_verification_email(email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def generate_random_username(length=10):
    letters_and_digits = ascii_letters + digits
    username = ''.join(choice(letters_and_digits) for _ in range(length))
    return username if not username_exists(username) else generate_random_username()


def get_user_by_user_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
