from  django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset = Course.objects.all(),widget=forms.HiddenInput)
class DropCourseForm(forms.Form):
    course = forms.CharField(widget=forms.HiddenInput)
