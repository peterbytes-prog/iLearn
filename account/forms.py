from django import forms
from students.models import Student
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name',  'last_name', 'email')

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('gender', 'date_of_birth',  'photo')
