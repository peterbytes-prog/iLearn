from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,related_name='student',on_delete=models.CASCADE)
    def __str__(self):
        return f"Student: {self.user.username}"
