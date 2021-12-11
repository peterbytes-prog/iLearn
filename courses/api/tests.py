from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from courses.models import *
from students.models import *
from .serializers import *

class TestApi(APITestCase):
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

        self.student2 = User.objects.create_user(
            username = 'Student Two',
            password = 'akloeicl889'
        )
        self.student2.save()


        self.MathSubject = Subject.objects.create(title='Math',slug='mathematics')
        self.math_101 = Course.objects.create(instructor=self.instructor1,
                                                    subject = self.MathSubject,
                                                    title = 'Math 101',
                                                    overview = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempo est laborum.',
                                                    slug = 'math_101'
                                                    )
        student_1_enrollment = Enrollment.objects.create(
            student = self.student1.student,
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
                                                    slug = 'english_225')

        self.client = APIClient()
    def test_subject_list(self):
        url = reverse('api:subject_list')
        response = self.client.get(url)
        ref = SubjectSerializer(Subject.objects.all(),many=True)
        self.assertEqual(response.data,ref.data)
    def test_subject_detail(self):
        url = reverse('api:subject_detail',kwargs={'pk':1})
        response = self.client.get(url)
        ref = SubjectSerializer(Subject.objects.get(pk=1),many=False)
        self.assertEqual(response.data,ref.data)
    def test_user_detail(self):
        url = reverse('api:user_detail',kwargs={'pk':self.student1.pk})
        client = APIClient()
        token = Token.objects.get(user__pk=self.student1.pk)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        ref = UserDetailSerializer(self.student1,many=False)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,ref.data)
        response = client.get(reverse('api:user_detail',kwargs={'pk':self.instructor1.pk}))
        self.assertEqual(response.status_code,403)

    def test_user_update(self):
        url = reverse('api:user_update',kwargs={'pk':self.student1.pk})
        client = APIClient()
        token = Token.objects.get(user__pk=self.student1.pk)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        self.assertEqual(response.status_code,405)
        response = client.put(url,data = {
            'username': 'Student_Test',
            'email':"Student@example.com",
            "password":'hsja180jj'
        })
        self.assertEqual(response.status_code,200)
        self.assertEqual(User.objects.get(pk=3).username,'Student_Test')
    def test_user_create(self):
        url = reverse('api:user_create')
        client = APIClient()
        new_user = {
            'username':'alloweduser',
            'password':'Hellanlka'
        }
        response = client.post(url,data=new_user)
        self.assertEqual(response.status_code,201)
        self.assertTrue(User.objects.get(username='alloweduser'))
        self.assertTrue(Student.objects.get(user__username='alloweduser'))
        self.assertTrue(Token.objects.get(user__username='alloweduser'))
    def test_user_enroll(self):
        url = reverse('api:course-enroll',kwargs={'pk':3})
        client = APIClient()
        ori = len(self.student1.student.enrollments.all())
        token = Token.objects.get(user__pk=self.student1.pk)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(url)
        self.assertTrue(len(self.student1.student.enrollments.all())==ori+1)
    def test_user_unenroll(self):
        url = reverse('api:course-drop',kwargs={'pk':1})
        client = APIClient()
        ori = len(self.student1.student.enrollments.all())
        token = Token.objects.get(user__pk=self.student1.pk)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(url)
        self.assertTrue(len(self.student1.student.enrollments.all())==ori-1)
    def test_course_contents(self):
        url = reverse('api:course-contents',kwargs={'pk':1})
        client = APIClient()
        token = Token.objects.get(user__pk=self.student1.pk)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        self.assertEqual(CourseWithModuleContentsSerializer(self.math_101).data,response.data)
