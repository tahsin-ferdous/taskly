from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    
    def __str__(self) -> str:
        return self.user.username
