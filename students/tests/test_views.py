from django.test import TestCase
from courses.models import *
from courses.views import *
from students.models import Student
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission


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

        self.MathSubject = Subject.objects.create(title='Math',slug='mathematics')
        self.math_101 = Course.objects.create(instructor=self.instructor1,
                                                    subject = self.MathSubject,
                                                    title = 'Math 101',
                                                    overview = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempo est laborum.',
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
        Content.objects.create(module=self.math_101_module_1,item=self.text_one)
        self.math_105 = Course.objects.create(instructor=self.instructor1,
                                                    subject = self.MathSubject,
                                                    title = 'Math 105',
                                                    overview = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempo est laborum.',
                                                    slug = 'math_105'
                                                    )
        self.EngSubject = Subject.objects.create(title='English',slug='english')
        self.english_101  = Course.objects.create(instructor=self.instructor2,
                                                    subject = self.EngSubject,
                                                    title = 'English 101',
                                                    overview = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempo est laborum.',
                                                    slug = 'english_101'
                                                    )
        self.english_225 = Course.objects.create(instructor=self.instructor2,
                                                    subject = self.EngSubject,
                                                    title = 'English 225',
                                                    overview = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempo est laborum.',
                                                    slug = 'english_225'
                                                    )
    def test_register_view(self):
        url = reverse('students:student_registration')
        success_url = reverse('students:student_course_list')
        new_student ={
            'username':'test_student',
            'password1':'nminikit',
            'password2':'nminikit'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        response = self.client.post(url,new_student)
        self.assertRedirects(response,success_url)
        pass
    def test_student_course_list_view(self):
        url = reverse('students:student_course_list')
        response = self.client.get(url)
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        print()
        self.assertEqual(str(response.context['object_list']),str(self.student1.course_set.all()))
    def test_student_enroll_to_course_view(self):
        # kwargs={'course':str(self.english_225.pk)}
        url = reverse('students:student_enroll_course')
        success_url = reverse('students:student_course_detail',args=[self.english_225.pk])
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        #inital length
        self.assertEqual(len(self.student1.enrollments.all()),1)
        response = self.client.post(url,{'course':str(self.english_225.pk)})
        self.assertEqual(len(self.student1.enrollments.all()),2)
        self.assertRedirects(response,success_url)
    def test_student_course_detail(self):
        url = reverse('students:student_course_detail',args=[self.math_101.pk])
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(str(response.context['object']),str(self.math_101))
        pass
    def test_drop_course_view(self):
        kwargs = {
            'pk':1
        }
        url = reverse('students:drop_course',kwargs=kwargs)
        success_url = reverse('courses:course_detail',kwargs={'slug':self.math_101.slug})
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(self.student1.enrollments.all()),1)
        response = self.client.post(url)
        self.assertRedirects(response,success_url)
        self.assertEqual(len(self.student1.enrollments.all()),0)
# #
