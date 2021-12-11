from django.db import models
from django.conf import settings
from django.urls import reverse
from PIL import Image as pImage
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='student', on_delete=models.CASCADE)

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
    feature = models.BooleanField(default=False,null=True)
    def __str__(self):
        return f"Student: {self.user.username}"
    def get_absolute_url(self):
        return reverse('profile:profile-detail',args=[self.pk])
    def save(self,*args,**kwargs):
        ins = super().save(*args,**kwargs)
        img = pImage.open(self.photo.path)
        img = img.resize((300,300))#pininterest ref
        img.save(self.photo.path)
