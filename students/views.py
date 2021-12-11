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
from assignments.models import *
from django import forms


from django.contrib.auth import login, authenticate
class StudentMixins(LoginRequiredMixin,):
    student = None
    enrollment = None
    def dispatch(self,request,pk=None,assignment_id=None,*args,**kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request,pk,assignment_id,*args,**kwargs)
        student = Student.objects.filter(user=request.user)
        if student:
            self.student = student[0]
        if pk:
            self.enrollment = get_object_or_404(Enrollment,student=self.student,course=Course.objects.get(pk=pk))
        return super().dispatch(request,pk,assignment_id,*args,**kwargs)

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
        student,created = Student.objects.get_or_create(user=self.request.user)
        self.course_enrollement = Enrollment.objects.get_or_create(student=student,course=self.course)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('students:student_course_detail',args=[self.course.id])
class StudentCourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(enrollments=self.request.user.student)
        return qs.filter(enrollments=self.request.user.student)
    pass
class StudentCourseDetailMixin(StudentMixins):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs = super().get_queryset()
        #if not in course redirect course info page
        student = self.student
        return qs.filter(course_enrollements__student__in=[student])
    pass
class StudentCourseDetailView(StudentCourseDetailMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['page'] = 'module'
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            modules = course.modules.all()
            if modules:
                context['module'] = course.modules.all()[0]
            else:
                context['module'] = []
        return context

class StudentCourseAssignmentDetailView(StudentCourseDetailMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['page'] = 'assignment'
        if 'assignment_id' in self.kwargs:
            context['assignment'] = course.assignments.get(id=self.kwargs['assignment_id'])
        else:
            assignment = course.assignments.all()
            if assignment:
                context['assignment'] = assignment[0]
            else:
                context['assignment'] = []
        if context['assignment']:
            context['attempted'] = Attempt.objects.filter(assignment=context['assignment'],enrollment=self.enrollment)
            if context['attempted']:
                context['attempted_highest'] = sorted(context['attempted'],key=lambda x:x.get_grade()['total'])[-1]
        return context


class StudentCourseDelete(LoginRequiredMixin,TemplateResponseMixin, View):
    template_name='students/student/drop.html'
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        qs = qs.filter(enrollments = request.user.student)
        return qs
    def get(self,request,pk):
        course = get_object_or_404(Course,id=pk)
        form = DropCourseForm(data={'course':course.id})
        return self.render_to_response({'course':course,'form':form})
    def post(self,request,pk):
        course = get_object_or_404(Course,id=pk)
        form = DropCourseForm(data={'course':course.id})
        if form.is_valid():
            student = request.user.student
            enroll = Enrollment.objects.filter(course=course,student = student)
            if enroll:
                enroll.delete()
        return redirect(reverse_lazy('courses:course_detail',kwargs={'slug':course.slug}))
