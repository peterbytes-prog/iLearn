from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from students.models import Student
# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject  = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student,related_name='courses_joined',blank=True)# TODO:  change model sttructure later  student model in of itself
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'
    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={
    "model__in":(
    'text',
    'video',
    'image',
    'file'
    )
    })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True, for_fields=['module'])
    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="%(class)s_related")
    title = models.CharField(max_length=250)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    def render(self):
        return render_to_string(f"courses/content/{self._meta.model_name}.html",{'item':self})
    pass

class Text(ItemBase):
    content = models.TextField()
    pass
class File(ItemBase):
    file = models.FileField(upload_to='files')
    pass
class Image(ItemBase):
    file = models.FileField(upload_to='images')
    pass
class Video(ItemBase):
    url = models.URLField()
    pass

#
