from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,related_name='student',on_delete=models.CASCADE)

    gender_choice = [
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    ]
    gender = models.CharField(
    max_length=6,
    choices=gender_choice,
    default='Other'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',default='users/user_icon.png',
                              blank=False)
    def __str__(self):
        return f"Student: {self.user.username}"
