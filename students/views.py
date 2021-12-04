from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from .forms import CourseEnrollForm, DropCourseForm
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateResponseMixin, View
from courses.models import *
from .models import Student
from django import forms


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
        self.course_enrollement = self.course.course_enrollements
        if not self.course_enrollement:
            self.course_enrollement = Enrollment.objects.create(course=self.course)
        student,created = Student.objects.get_or_create(user=self.request.user)
        self.course_enrollement.students.add(student)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:student_course_detail',args=[self.course.id])
class StudentCourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        student = Student.objects.filter(user__in=[self.request.user])
        if student:
            qs = student[0].enrollments.all()
        else:
            qs = []
        return qs
    pass
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs = super().get_queryset()
        #if not in course redirect course info page
        student = Student.objects.filter(user__in=[self.request.user])
        return qs.filter(course_enrollements__students__in=student)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            modules = course.modules.all()
            if modules:
                context['module'] = course.modules.all()[0]
            else:
                context['module'] = []
        return context

class StudentCourseDelete(LoginRequiredMixin,TemplateResponseMixin, View):
    template_name='students/student/drop.html'
    def get(self,request,pk):
        course = get_object_or_404(Course,id=pk)
        form = DropCourseForm(data={'course':course.id})
        return self.render_to_response({'course':course,'form':form})
    def post(self,request,pk):
        course = get_object_or_404(Course,id=pk)
        form = DropCourseForm(data={'course':course.id})
        if form.is_valid():
            student = Student.objects.filter(user__in=[self.request.user])
            enroll = course.course_enrollements.students.remove(*student)
        return redirect(reverse_lazy('courses:course_detail',kwargs={'slug':course.slug}))
