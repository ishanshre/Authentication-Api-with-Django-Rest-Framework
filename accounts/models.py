from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    email_confirmed = models.BooleanField(_("email confirmed"),default=False)

    def __str__(self):
        return self.username
    


class GENDER_CHOICES(models.TextChoices):
    MALE = "M",'Male'
    FEMALE = "F",'Female'
    OTHER = "O",'Others'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="user/profile", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES.choices, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username.title()}'s Profile"


