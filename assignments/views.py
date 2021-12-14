from django.shortcuts import render,  redirect,  get_object_or_404
from django.http import HttpResponseForbidden,  HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin,  PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin,  View
from django.views.generic.edit import CreateView,  UpdateView,  DeleteView
from django.views.generic.detail import DetailView
from django.forms.models import modelform_factory
from courses.models import *
from .models import *
from .forms import CourseAssignmentFormSet,  ChoiceFormSet, QuestionForm
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
# Create your views here.


class StudentTestPage(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignments/student/test_page.html'
    student = None
    enrollment = None
    def dispatch(self, request, course_id, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, course_id, pk, *args, **kwargs)
        self.course = get_object_or_404(Course, pk=course_id)
        self.student = get_object_or_404(Student, user=request.user)
        self.enrollment = get_object_or_404(Enrollment, student=self.student, course=self.course)
        self.assignment = get_object_or_404(Assignment, pk=pk)
        return super().dispatch(request, course_id, pk, *args, **kwargs)
    def post(self, request, course_id, pk, *args, **kwargs):
        student = self.student
        object = self.get_object()
        assignment_questions = object.assignment_questions.filter(id__in=[str(i) for i in request.POST.keys() if i!='csrfmiddlewaretoken'])
        attempt_ins = Attempt.objects.create(
            assignment = object,
            enrollment = self.enrollment
        )
        for question in assignment_questions:
            joined_choice = question.question_choices.filter(id__in = request.POST.getlist(str(question.pk)))
            for choice in joined_choice:
                attempt_choices = AttemptChoice.objects.create(
                    attempt = attempt_ins,
                    choice = choice
                )
        return redirect(reverse('courses:assignments:test_review_page', args=[course_id, object.id, attempt_ins.pk]))


class StudentTestReviewPage(LoginRequiredMixin, DetailView):
    model = Attempt
    template_name = 'assignments/student/test_review_page.html'
    student = None
    enrollment = None
    def dispatch(self, request, course_id, assignment_id, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, course_id, assignment_id, pk, *args, **kwargs)
        self.course = get_object_or_404(Course, pk=course_id)
        self.student = get_object_or_404(Student, user=request.user)
        self.enrollment = get_object_or_404(Enrollment, student=self.student, course=self.course)
        self.assignment = get_object_or_404(Assignment, pk=assignment_id)
        return super().dispatch(request, course_id, pk, *args, **kwargs)
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(enrollment=self.enrollment, assignment=self.assignment)
        return qs
    def get_context_data(self, *arg, **kwargs):
        ctx = super().get_context_data(*arg, **kwargs)
        ctx['attempted'] = self.get_queryset()
        return ctx


class CourseAssignmentManageMixins(LoginRequiredMixin, PermissionRequiredMixin):
    course = None
    assignment = None
    question = None
    enrollment = None
    permission_required = ('courses.can_view_course', 'courses.can_view_content')
    def dispatch(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        #check for authentication
        self.course = get_object_or_404(Course, pk=course_id)
        if assignment_id:
            self.assignment = get_object_or_404(Assignment, pk=assignment_id)
        if question_id:
            self.question = get_object_or_404(Question, pk=question_id, assignment=self.assignment)
        # self.assignment = self.course.course_enrollements.assignments.filter(pk=assignment_id)
        return super().dispatch(request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs)

class CourseAssignmentListDetailView(CourseAssignmentManageMixins, TemplateResponseMixin, View):
    """ModuleContentListView. for course_assignment_question_list"""
    template_name = 'assignments/course/assignment_list_detail.html'
    def get(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        if not self.assignment:
            self.assignment = self.course.assignments.first()
        return self.render_to_response({"enrollment":self.enrollment, 'assignment':self.assignment, 'course':self.course})
    def post(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        if request.POST.get('delete_q'):
            question = get_object_or_404(Question, id=request.POST.get('delete_q'))
            question.delete()
        return redirect(request.path)


class QuestionCreateUpdateDetailView(CourseAssignmentManageMixins, TemplateResponseMixin, View):
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'assignments/manage/question/form.html'
    def get(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        question_form = QuestionForm(instance=self.question)
        choice_formset = ChoiceFormSet(instance=self.question)
        return self.render_to_response({'question_form':question_form, 'choice_formset':choice_formset, 'object':self.question})

    def post(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        question_form = QuestionForm(instance=self.question, data=request.POST)
        choice_formset = ChoiceFormSet(instance=self.question, data=request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.assignment = self.assignment
            choice_formset = ChoiceFormSet(instance=question,  data=request.POST)
            if choice_formset.is_valid():
                question.save()
                choices = choice_formset.save()
            else:
                return self.render_to_response({'question_form':question_form, 'choice_formset':choice_formset, 'object':self.question})
        else:
            return self.render_to_response({'question_form':question_form, 'choice_formset':choice_formset, 'object':self.question})
        if request.POST.get('next'):
            return redirect(reverse_lazy('courses:assignments:assignment_question_create', args=[self.course.pk, self.assignment.pk]))
        return redirect(reverse_lazy('courses:assignments:course_a_assignment_question_list', args=[self.course.pk, self.assignment.pk]))


class CourseAssignmentListUpdateView(CourseAssignmentManageMixins, TemplateResponseMixin, View):
    """list assignments for instructors"""
    template_name = 'assignments/course/assignment_list_update.html'
    def get_formset(self, data=None):
        course_assignment_form = CourseAssignmentFormSet(instance=self.course, data=data)
        return course_assignment_form
    def get(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course, 'formset':formset})
    def post(self, request, course_id=None, assignment_id=None, question_id=None, *args, **kwargs):
        formset = CourseAssignmentFormSet(instance=self.course, data=request.POST)
        if formset.is_valid():
            try:
                formset = formset.save()
            except:
                formset = formset.save(commit=False)
                for f in formset:
                    f.instructor = request.user.instructor
                    f.slug = slugify(f.title)
                    f.save()
            return redirect(reverse_lazy('courses:manage_course_list'))
        else:
            return self.render_to_response({'course':self.course, 'formset':formset})
