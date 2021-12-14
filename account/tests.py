from django.test import TestCase
from django.test import TestCase
from courses.models import *
from courses.views import *
from students.models import Student
from django.urls import reverse
from django.contrib.auth.models import User,  Group,  Permission


class TestView(TestCase):
    def setUp(self):
        #setup 4 users two students and two instructor
        self.instructor1 = User.objects.create(
            username = 'Instructor One'
        )
        self.instructor1.set_password('hsja180jj')
        self.instructor1.save()
        self.instructor1 = Instructor.objects.create(user=self.instructor1)
        self.instructor1.save()
        self.instructor2 = User.objects.create_user(
            username = 'Instructor Two',
            password = 'akloeicl889'
        )
        self.instructor2.save()
        self.instructor2 = Instructor.objects.create(user=self.instructor2)
        self.instructor2.save()
        #now students
        self.student1 = User.objects.create(
            username = 'Student One'
        )
        self.student1.set_password('hsja180jj')
        self.student1.save()
        self.student1 = self.student1.student

        self.student2 = User.objects.create_user(
            username = 'Student Two',
            password = 'akloeicl889'
        )
        self.student2.save()
        self.student2 = self.student2.student

        self.MathSubject = Subject.objects.create(title='Math', slug='mathematics')
        self.math_101 = Course.objects.create(instructor=self.instructor1,
                                                    subject = self.MathSubject,
                                                    title = 'Math 101',
                                                    overview = 'Lorem ipsum dolor sit amet,  consectetur adipisicing elit,  sed do eiusmod tempo est laborum.',
                                                    slug = 'math_101'
                                                    )
        student_1_enrollment = Enrollment.objects.create(
            student = self.student1,
            course = self.math_101
        )
        #modules math_101
        self.math_101_module_1 = {
        'course':self.math_101,
        'title':'module one',
        'description':'module one description'
        }
        self.math_101_module_1 = Module.objects.create(**self.math_101_module_1)

        self.math_101_module_2 = {
        'course':self.math_101,
        'title':'module two',
        'description':'module two description'
        }
        self.math_101_module_2 = Module.objects.create(**self.math_101_module_2)

        #module one text content
        self.text_one = {
            'instructor':self.instructor1,
            'title':'Text Content One',
            'content':'Math 101 module One Text Content One'
        }
        self.text_one = Text.objects.create(**self.text_one)
        Content.objects.create(module=self.math_101_module_1, item=self.text_one)
        self.math_105 = Course.objects.create(instructor=self.instructor1,
                                                    subject = self.MathSubject,
                                                    title = 'Math 105',
                                                    overview = 'Lorem ipsum dolor sit amet,  consectetur adipisicing elit,  sed do eiusmod tempo est laborum.',
                                                    slug = 'math_105'
                                                    )
        self.EngSubject = Subject.objects.create(title='English', slug='english')
        self.english_101  = Course.objects.create(instructor=self.instructor2,
                                                    subject = self.EngSubject,
                                                    title = 'English 101',
                                                    overview = 'Lorem ipsum dolor sit amet,  consectetur adipisicing elit,  sed do eiusmod tempo est laborum.',
                                                    slug = 'english_101'
                                                    )
        self.english_225 = Course.objects.create(instructor=self.instructor2,
                                                    subject = self.EngSubject,
                                                    title = 'English 225',
                                                    overview = 'Lorem ipsum dolor sit amet,  consectetur adipisicing elit,  sed do eiusmod tempo est laborum.',
                                                    slug = 'english_225'
                                                    )
    def test_profile_view(self):
        #test edit form accessibility
        url = reverse('profile:profile-detail', args=[self.student2.pk])
        login = self.client.login(username=self.student1.user.username,  password='hsja180jj')
        response = self.client.get(url)
        self.assertFalse(response.context.get('student_form', False))
        self.assertFalse(response.context.get('user_form', False))

        url = reverse('profile:profile-detail', args=[self.student1.pk])
        login = self.client.login(username=self.student1.user.username,  password='hsja180jj')
        response = self.client.get(url)
        self.assertTrue(response.context.get('student_form', True))
        self.assertTrue(response.context.get('user_form', True))

        pass
