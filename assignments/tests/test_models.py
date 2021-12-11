from django.test import TestCase
from courses.models import *
from courses.views import *
from students.models import Student
from django.urls import reverse
from assignments.models import Assignment,Question,TextChoice,Attempt,AttemptChoice
from django.contrib.auth.models import User, Group, Permission

class TestModels(TestCase):
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
        self.assignment1 = Assignment.objects.create(
            title='Assignment One',
            overview='Lorem ipsum dolor sit amet, consectetur adipisicing elit.',
            slug='assignment-one',
            weight=25.00,
            course=self.math_101
        )

        self.ass_1_q_1 = Question.objects.create(
            assignment = self.assignment1,
            order = 1,
            question = "Question One multiple false",
            multiple = False
        )
        self.ass_1_q_1_c_1 = TextChoice.objects.create(
            question = self.ass_1_q_1,
            order = 1,
            point = 1,
            content = 'Choice One'
        )
        self.ass_1_q_1_c_2 = TextChoice.objects.create(
            question = self.ass_1_q_1,
            order = 2,
            point = 0,
            content = 'Choice Two'
        )
        self.ass_1_q_1_c_3 = TextChoice.objects.create(
            question = self.ass_1_q_1,
            order = 3,
            point = 0,
            content = 'Choice Three'
        )

        self.ass_1_q_2 = Question.objects.create(
            assignment = self.assignment1,
            order = 2,
            question = "Question Two multiple true",
            multiple = True
        )

        self.ass_1_q_2_c_1 = TextChoice.objects.create(
            question = self.ass_1_q_2,
            order = 1,
            point = 0.75,
            content = 'Choice One'
        )
        self.ass_1_q_2_c_2 = TextChoice.objects.create(
            question = self.ass_1_q_2,
            order = 2,
            point = -5,
            content = 'Choice Two'
        )
        self.ass_1_q_2_c_3 = TextChoice.objects.create(
            question = self.ass_1_q_2,
            order = 3,
            point = 0.5,
            content = 'Choice Three'
        )
        #managing attempts
        self.student_1_ass_1_attempt_1 = Attempt.objects.create(
            assignment = self.assignment1,
            enrollment = Enrollment.objects.get(course=self.math_101,student=self.student1),
        )
        # choose choice 1 for question and choice 1,2 for question 2,
        attempt_choices_q1 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_1,
            choice = self.ass_1_q_1_c_1
        )

        attempt_choices_q2_c1 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_1,
            choice = self.ass_1_q_2_c_2
        )
        attempt_choices_q2_c2 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_1,
            choice = self.ass_1_q_2_c_3
        )
        #attempt 2
        self.student_1_ass_1_attempt_2 = Attempt.objects.create(
            assignment = self.assignment1,
            enrollment = Enrollment.objects.get(course=self.math_101,student=self.student1),
        )
        # choose choice 1 for question and choice 1,3 for question 2,
        attempt2_choices_q1 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_2,
            choice = self.ass_1_q_1_c_1
        )

        attempt2_choices_q2_c1 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_2,
            choice = self.ass_1_q_2_c_1
        )
        attempt2_choices_q2_c2 = AttemptChoice.objects.create(
            attempt = self.student_1_ass_1_attempt_2,
            choice = self.ass_1_q_2_c_3
        )
        self.assignment2 = Assignment.objects.create(
            title='Assignment Two',
            overview='Lorem ipsum dolor sit amet, consectetur adipisicing elit.',
            slug='assignment-two',
            weight=55.00,
            course=self.math_101
        )
    def test_asssignment_model_string(self):
        self.assertEqual(
            str(self.assignment1),
            f"{self.math_101.title}, Assignment: {self.assignment1.title}"
            )
    def test_question_max_point(self):
        self.assertEqual(self.ass_1_q_1.total_point(),1)
        self.assertEqual(self.ass_1_q_2.total_point(),1.25)

    def test_question_model_string(self):
        self.assertEqual(
            str(self.ass_1_q_1),
            f"Assignment: {self.assignment1.title}, question {self.ass_1_q_1.order}"
            )
    def test_choice_model_string(self):
        self.assertEqual(
            str(self.ass_1_q_1_c_1),
            f"{str(self.ass_1_q_1)}, choice: {self.ass_1_q_1_c_1.order}, point: {self.ass_1_q_1_c_1.point}"
            )
    def test_attempts(self):
        student1_enrollment_assignment = self.student1.enrollments.get(course=self.math_101).course.assignments.all()
        self.assertEqual(len(student1_enrollment_assignment),2)
        assignment_one_attempts = self.student1.enrollments.get(course=self.math_101).assignment_attempts.all()
        self.assertEqual(sum([float(i.get_grade()['total']) for i in assignment_one_attempts]),3.25)
#
