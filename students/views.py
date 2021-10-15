from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from courses.models import *

from django.contrib.auth import login, authenticate

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('students:student_course_list')

    def form_valid(self,form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request,user)
        return result
class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    form_class = CourseEnrollForm
    course = None
    template_name = 'students/student/registration.html'
    def form_valid(self,form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        print('form submitted')
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('students:student_course_detail',args=[self.course.id])
class StudentCourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user ])
    pass
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
        return context
