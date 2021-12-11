from django.test import TestCase
from courses.models import *
from courses.views import *
from students.models import Student
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission

class TestCourseView(TestCase):
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
    def test_course_owner_view(self):
        url = 'courses/mine/'
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), ins.user.username)
        self.assertEqual(str(response.context['course_list']),str(ins.courses_created.all()))
        self.assertTemplateUsed(response,'courses/manage/course/list.html')
    def test_cms_access_authentications(self):
        logout = self.client.logout()
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertRedirects(response,'/accounts/login/?next=/course/mine/')
        #login as student
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertEqual(response.status_code,403)
    def test_create_view(self):
        url = reverse('courses:course_create')
        success_url = reverse('courses:manage_course_list')
        # test login required redirect
        logout = self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'courses/manage/course/form.html')
        #test success_url
        response = self.client.post(url,{
            'subject':'1',
            'title':'Calculus 101',
            'slug':'calculus-101',
            'overview':'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'
        })
        self.assertRedirects(response,success_url)
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertEqual(str(response.context['user']), ins.user.username)
        self.assertEqual(str(response.context['course_list']),str(ins.courses_created.all()))
    def test_edit_view(self):
        first_course = self.instructor1.courses_created.get(pk=1)
        url = reverse('courses:course_edit',kwargs={'pk':str(first_course.pk)})
        success_url = reverse('courses:manage_course_list')
        # test login required redirect
        logout = self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'courses/manage/course/form.html')
        #test success_url
        response = self.client.post(url,{
            'subject':'1',
            'title':'Math 101 Version Two',
            'slug':'math-101-version-two',
            'overview':'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'
        })
        self.assertRedirects(response,success_url)
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertEqual(str(response.context['user']), ins.user.username)
        self.assertEqual(str(response.context['course_list']),str(ins.courses_created.all()))
        self.assertEqual(ins.courses_created.get(pk=1).title,'Math 101 Version Two')
    def test_delete_view(self):
        first_course = self.instructor1.courses_created.get(pk=1)
        url = reverse('courses:course_delete',kwargs={'pk':str(first_course.pk)})
        success_url = reverse('courses:manage_course_list')
        # test login required redirect
        logout = self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'courses/manage/course/delete.html')
        #test success_url
        response = self.client.post(url)
        self.assertRedirects(response,success_url)
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertEqual(str(response.context['user']), ins.user.username)
        self.assertEqual(str(response.context['course_list']),str(ins.courses_created.all()))
        self.assertEqual(len(ins.courses_created.all()),1)
    def test_module_create_and_update_view(self):
        first_course = self.instructor1.courses_created.get(pk=1)
        url = reverse('courses:course_module_update',kwargs={'pk':str(first_course.pk)})
        success_url = reverse('courses:manage_course_list')
        # test login required redirect
        logout = self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'courses/manage/module/formset.html')
    def test_module_content_create_view(self):
        kwargs = {
            'module_id':str(self.math_101_module_1.pk),
            'model_name':'text'
        }
        url = reverse('courses:module_content_create',kwargs=kwargs)
        success_url = reverse('courses:module_content_list',kwargs={'module_id':self.math_101_module_1.pk})
        logout = self.client.logout()
        #test Login Required
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)

        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'courses/manage/content/form.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url,{
            'instructor':str(self.instructor1.pk),
            'title':'Text Content Two',
            'content':'Math 101 module One Text Content Two'
        })
        self.assertRedirects(response,success_url)
        self.assertEqual(len(self.math_101_module_1.contents.all()),2)

    def test_module_content_list(self):
        first_course = self.instructor1.courses_created.get(pk=1)
        kwargs = {
            'module_id':str(self.math_101_module_1.pk)
        }
        url = reverse('courses:module_content_list',kwargs=kwargs)
        logout = self.client.logout()
        #test Login Required
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')

        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)

        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'courses/manage/module/content_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['module'].contents.all()),len(self.math_101_module_1.contents.all()))
    def test_module_content_update_view(self):
        kwargs = {
            'module_id':str(self.math_101_module_1.pk),
            'model_name':'text',
            'id':'1'
        }
        url = reverse('courses:module_content_update',kwargs=kwargs)
        success_url = reverse('courses:module_content_list',kwargs={'module_id':self.math_101_module_1.pk})
        logout = self.client.logout()
        #test Login Required
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)

        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'courses/manage/content/form.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url,{
            'instructor':str(self.instructor1.pk),
            'title':'Text Content V2',
            'content':'Math 101 module One Text Content Two'
        })
        self.assertRedirects(response,success_url)
        self.assertEqual(len(self.math_101_module_1.contents.all()),1)
        self.assertEqual(Text.objects.get(pk=1).title,'Text Content V2')
    def test_module_content_delete_view(self):
        kwargs = {
            'id':1
        }
        url = reverse('courses:module_content_delete',kwargs=kwargs)
        success_url = reverse('courses:module_content_list',kwargs={'module_id':self.math_101_module_1.pk})
        logout = self.client.logout()
        #test Login Required
        response = self.client.get(url)
        self.assertRedirects(response,f'/accounts/login/?next={url}')
        #test only instructor access
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        #
        #test template
        logout = self.client.logout()
        ins = self.instructor1
        login = self.client.login(username=ins.user.username, password='hsja180jj')
        response = self.client.post(url)
        self.assertRedirects(response,success_url)
        self.assertEqual(len(self.math_101_module_1.contents.all()),0)
    def test_course_list_by_subject(self):
        kwargs = {
            'subject':'mathematics'
        }
        url = reverse('courses:course_list_subject',kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(len(response.context['subjects']),2)#Math,English
        self.assertEqual(len(response.context['subjects']),2)#math 101,math 102
    def test_course_detail_view(self):
        logout = self.client.logout()
        kwargs = {
            'slug':'math_101'
        }
        url = reverse('courses:course_detail',kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(str(response.context['course']),str(self.math_101))
        self.assertIn('enroll_form',response.context)
        login = self.client.login(username=self.student1.user.username, password='hsja180jj')
        response = self.client.get(url)
        self.assertFalse(response.context.get('enroll_form',False))
        self.assertTrue(response.context.get('is_student'))
