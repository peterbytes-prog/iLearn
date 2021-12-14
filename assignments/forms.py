from django.forms.models import inlineformset_factory
from django import forms
from courses.models import Course, Enrollment
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from .models import (Assignment, Course, Question, TextChoice)


CourseAssignmentFormSet = inlineformset_factory(
    Course,
    Assignment,
    fields = [
        'title',
        'overview',
        'weight',
        'opens',
        'closes',
        'time_limit',
    ],
    extra=2,
    can_delete=True,
)
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['order', 'question', 'multiple']
    pass
ChoiceFormSet = inlineformset_factory(
    Question,
    TextChoice,
    fields = [
        'order',
        'content',
        'point'
    ],
    extra=4,
    can_delete=True,
    max_num=5,  validate_max=True,
    min_num=1,  validate_min=True
)
