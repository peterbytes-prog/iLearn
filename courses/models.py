from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from students.models import Student
from ckeditor.fields import RichTextField
from PIL import Image as pImage
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    feature = models.BooleanField(default=False,null=True)
    photo = models.ImageField(upload_to='subjects/%Y/%m/%d/',default='subjects/subjects_icon.png',
                              blank=False)
    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        ins = super().save(*args,**kwargs)
        img = pImage.open(self.photo.path)
        img.thumbnail((500,500))#pininterest ref
        img.save(self.photo.path)

class Enrollment(models.Model):
    student = models.ForeignKey(Student,related_name='enrollments',on_delete=models.CASCADE)# TODO:  change model sttructure later  student model in of itself
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey('Course',on_delete=models.CASCADE, related_name='course_enrollements')
    def __str__(self):
        return f"Enrollment For: {self.course}"
    class Meta:
        unique_together = ('student','course')
class Course(models.Model):
    instructor = models.ForeignKey('Instructor', related_name='courses_created', on_delete=models.CASCADE)
    subject  = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)
    enrollments = models.ManyToManyField(Student,through='Enrollment')
    feature = models.BooleanField(default=False,null=True)
    photo = models.ImageField(upload_to='courses/%Y/%m/%d/',default='courses/course_icon.png',
                              blank=False)

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        ins = super().save(*args,**kwargs)
        img = pImage.open(self.photo.path)
        img.thumbnail((500,500))#pininterest ref
        img.save(self.photo.path)

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
    instructor = models.ForeignKey('Instructor',on_delete=models.CASCADE,related_name="%(class)s_related")
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
    content = RichTextField(blank=True,null=True)
    # content = models.TextField()
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
class Instructor(models.Model):
    user = models.OneToOneField(User,related_name='instructor',on_delete=models.CASCADE)
    feature = models.BooleanField(default=False,null=True)
    def save(self,*args,**kwargs):

        instructors, created = Group.objects.get_or_create(name = "instructors")
        if created:
            permissions_list = {
                'Course':[
                    ('can_add_course',"Can add course"),
                    ('can_change_course',"Can change course"),
                    ('can_delete_course',"Can delete course"),
                    ('can_view_course',"Can view course")
                ],
                'Content':[
                    ('can_add_content',"Can add content"),
                    ('can_change_content',"Can change content"),
                    ('can_delete_content',"Can delete content"),
                    ('can_view_content',"Can view content")
                ],
                'File':[
                    ('can_add_file',"Can add file"),
                    ('can_change_file',"Can change file"),
                    ('can_delete_file',"Can delete file"),
                    ('can_view_file',"Can view file")
                ],
                'Image':[
                    ('can_add_image',"Can add image"),
                    ('can_change_image',"Can change image"),
                    ('can_delete_image',"Can delete image"),
                    ('can_view_image',"Can view image")
                ],
                'Text':[
                    ('can_add_text',"Can add text"),
                    ('can_change_text',"Can change text"),
                    ('can_delete_text',"Can delete text"),
                    ('can_view_text',"Can view text")
                ],
                'Video':[
                    ('can_add_video',"Can add video"),
                    ('can_change_video',"Can change video"),
                    ('can_delete_video',"Can delete video"),
                    ('can_view_video',"Can view video")
                ]
            }
            for model in permissions_list:
                if model == 'Video':
                    ct = ContentType.objects.get_for_model(Video)
                elif model == 'Text':
                    ct = ContentType.objects.get_for_model(Text)
                elif model == 'File':
                    ct = ContentType.objects.get_for_model(File)
                elif model == 'Image':
                    ct = ContentType.objects.get_for_model(Image)
                elif model == 'Text':
                    ct = ContentType.objects.get_for_model(Text)
                elif model == 'Content':
                    ct = ContentType.objects.get_for_model(Content)
                elif model == 'Course':
                    ct = ContentType.objects.get_for_model(Course)
                for perm in permissions_list[model]:
                    permission = Permission.objects.create(
                        codename=perm[0],
                        name=perm[1],
                        content_type=ct
                        )
                    instructors.permissions.add(permission)
        self.user.groups.add(instructors)
        self.user.is_staff = True
        self.user.save()
        super().save(*args,**kwargs)
        pass

    def __str__(self):
        return f"Instructor: {self.user.username}"

    pass
