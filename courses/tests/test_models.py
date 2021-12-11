from django.test import TestCase
from students.models import Student
from courses.models import *
from django.contrib.auth.models import User,Permission
from django.db.utils import IntegrityError


class TestModels(TestCase):
    def setUp(self):
        #setup 4 users two students and two instructor
        self.instructor1 = User.objects.create_user(
            username = 'Instructor One',
            password = 'hsja180jj'
        )
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
        self.student1 = User.objects.create_user(
            username = 'Student One',
            password = 'hsja180jj'
        )
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
        pass
    def test_students(self):
        students = Student.objects.all()
        self.assertEqual(len(students),4)
        pass
    def test_intructors(self):
        instructors = Instructor.objects.all()
        self.assertEqual(len(instructors),2)
        self.assertEqual(len(Course.objects.all()),4)
        self.assertEqual(len(self.instructor2.courses_created.all()),2)
        self.assertEqual(len(self.instructor1.courses_created.all()),2)
    def test_students_and_enrollments(self):
        self.assertEqual(len(self.math_101.course_enrollements.all()),1)
        student_1_enrollment = Enrollment.objects.create(
            student = self.student1,
            course = self.math_101
        )
        student_2_enrollment = Enrollment.objects.create(
            student = self.student2,
            course = self.math_101
        )
        self.assertEqual(len(self.math_101.course_enrollements.all()),3)
