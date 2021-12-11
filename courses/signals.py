from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment,Course
from rest_framework.authtoken.models import Token
from students.models import Student

@receiver(post_save, sender=Course)
def create_course_enrollment(sender, instance, created, **kwargs):
    if created:
        Enrollment.objects.create(
            student = instance.instructor.user.student,
            course = instance
        )

@receiver(post_save, sender=User)
def create_course_enrollment(sender, instance, created, **kwargs):
    if created:
        pass
        #create new student automatically
        student,created = Student.objects.get_or_create(user=instance)
        # generate token automatically
        Token.objects.create(user=instance)
