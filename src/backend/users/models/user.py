from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, validators=[validate_email])
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.jpg')
    biography = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True)

    def get_username(self):
        return self.username
