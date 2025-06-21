from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        max_length=2000,
        blank=True,
        default=''
    )
    name = models.CharField(max_length=32, default='')
    avatar = models.ImageField(upload_to='userprofiles')
    links_instagram = models.CharField(max_length=30, blank=True, null=True)
    links_github = models.CharField(max_length=30, blank=True, null=True)
    links_linkedin = models.CharField(max_length=30, blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
  
    def __str__(self):
        return self.user.username