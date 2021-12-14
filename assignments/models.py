from django.db import models
import datetime
from courses.models import *
from courses.fields import OrderField
from django.template.loader import render_to_string
from ckeditor.fields import RichTextField
# Create your models here.


class Assignment(models.Model):
    # instructor = models.ForeignKey(Instructor,  related_name='assignments_created',  on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200,  unique=True)
    created = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5,  decimal_places=3)
    course = models.ForeignKey(Course, related_name='assignments',  on_delete=models.CASCADE)
    opens = models.DateTimeField(blank=True, null=True, help_text='YYYY-MM-DD HH:MM:SS')
    closes = models.DateTimeField(blank=True, null=True, help_text='YYYY-MM-DD HH:MM:SS')
    time_limit = models.DurationField(default=datetime.timedelta(days=0, hours=1,  minutes=0), help_text='hh:mm:ss')
    attempts = models.ManyToManyField(
        Enrollment,
        through='Attempt'
    )
    def __str__(self):
        return f"{self.course.title}, Assignment: {self.title}"
    def get_total(self):
        return sum([i.total_point() for i in self.assignment_questions.all()])
class Attempt(models.Model):
    #just a manual many to many to keep traack of student attempted assignment
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, related_name='assignment_attempts',  on_delete=models.CASCADE)
    choice = models.ManyToManyField('TextChoice', through='AttemptChoice')
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering =['-created']
        get_latest_by= ['-created']
    def __str__(self):
        return f"Attempt: {self.pk}"
    def get_grade(self):
        #because a total can be negative we need to iterate over each question and it choice for the attempts
        #get all the questions set for this assignment
        detail = {
            "total": 0,
            "info":[

            ]
        }
        questions = self.assignment.assignment_questions.all()
        for question in questions:
            selected_attempt_question_choice = self.choice.filter(question=question)
            question_actual_score = sum([i.point for i in selected_attempt_question_choice])
            question_grade_score = max(question_actual_score, 0)
            temp ={
                'id':question.pk,
                'act_score':float(question_actual_score)
            }
            detail['info'].append(temp)
            detail['total'] += question_grade_score
        return detail


class Question(models.Model):
    assignment = models.ForeignKey('Assignment', related_name='assignment_questions', on_delete=models.CASCADE)
    order = OrderField(blank=True,  for_fields=['assignment'])
    question = RichTextField()
    multiple = models.BooleanField(default=False, help_text='allow selecting multiple choices?')
    def __str__(self):
        return f"Assignment: {self.assignment.title}, question {self.order}"
    def get_score(self):
        pass
    def total_point(self):
        return sum([i.point for i in self.question_choices.all() if i.point>=0])
class Choice(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
    "model__in":(
    'TextChoice',
    )
    })
    object_id = models.PositiveIntegerField()
    choice = GenericForeignKey('content_type', 'object_id')
class ChoiceBase(models.Model):
    question = models.ForeignKey('Question', related_name='question_choices', on_delete=models.CASCADE)
    order = models.CharField(max_length=5, blank=True)
    point = models.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        abstract = True
    def __str__(self):
        return f"{str(self.question)}, choice: {self.order}, point: {self.point}"
    def render_intructor(self):
        return render_to_string(f"assignments/manage/choice/{self._meta.model_name}.html", {'item':self, 'instructor':True})
    def render(self, attempt=None):
        selected = False
        review = False
        if attempt:
            review = True
            if self in attempt.choice.all():
                selected = 'checked'
        return render_to_string(f"assignments/manage/choice/{self._meta.model_name}.html", {'item':self, 'selected':selected, 'review':review, 'instructor':False})

class TextChoice(ChoiceBase):
    content = RichTextField()

class AttemptChoice(models.Model):
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('choice', 'attempt')
