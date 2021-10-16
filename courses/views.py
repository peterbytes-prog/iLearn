from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.apps import apps
from django.forms.models import modelform_factory
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm


class OwnerMixin(object):
    """docstring for OwnerMixin."""
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        return qs.filter(owner=self.request.user)
    pass
class OwnerEditMixing(object):
    """docstring for OwnerEditMixing."""
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixing):
    template_name = 'courses/manage/course/form.html'
    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('courses:manage_course_list')
class ManageCourseListView(OwnerCourseMixin,ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
class CourseCreateView(OwnerCourseEditMixin,CreateView):
    """docstring for CourseCreateView."""
    permission_required = 'courses.add_course'
class CourseUpdateView(OwnerCourseEditMixin,UpdateView):
    """docstring for CourseUpdateView."""
    permission_required = 'courses.change_course'
class CourseDeleteView(OwnerCourseEditMixin,DeleteView):
    """docstring for CourseDeleteView."""
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
class CourseModuleUpdateView(TemplateResponseMixin,View):
    """docstring for CourseModuleUpdateView."""
    course = None
    template_name = 'courses/manage/module/formset.html'
    def dispatch(self,request,pk):
        self.course = get_object_or_404(Course,pk=pk)
        return super().dispatch(request,pk)
    def get_formset(self,data=None):
        course_modules_form = ModuleFormSet(instance=self.course,data=data)
        return course_modules_form
    def get(self,request,pk,*args,**kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course,'formset':formset})
    def post(self,request,pk,*args,**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('courses:manage_course_list'))
        else:
            return self.render_to_response({'course':self.course,'formset':formset})
    pass
class ContentCreateUpdateView(TemplateResponseMixin,View):
    template_name = 'courses/manage/content/form.html'
    model = None
    module = None
    obj = None
    def get_model(self,model_name):
        if model_name in ['text','video','image','file']:
            model = apps.get_model(app_label='courses',model_name=model_name)
            return model
        else:
            return None
    def get_form(self,model,*args,**kwargs):
        Form = modelform_factory(model,exclude=['owner','order','created','updated'])
        return Form(*args,**kwargs)
    def dispatch(self,request,module_id,model_name,id=None):
        self.module = get_object_or_404(Module,id=module_id,course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            obj = get_object_or_404(self.model,id=id,owner=request.user)
        return super().dispatch(request,module_id,model_name,id)
    def get(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model,instance=self.obj)
        return self.render_to_response({'form':form,'object':self.obj})
    def post(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model,
                                instance=self.obj,
                                data = request.POST,
                                files = request.FILES
                                )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,item=obj)
            return redirect(reverse_lazy('courses:module_content_list',kwargs={'module_id':self.module.id}))
        return self.render_to_response({'form':form,'object':self.obj})
    pass
class ContentDeleteView(DeleteView):
    def post(self,request,id):
        content = get_object_or_404(Content,id=id,module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect(reverse_lazy('courses:module_content_list',kwargs={'module_id':module.id}))
class ModuleContentListView(TemplateResponseMixin,View):
    """docstring for ModuleContentListView."""
    template_name = 'courses/manage/module/content_list.html'
    def get(self,request,module_id):
        module = get_object_or_404(Module,id=module_id,course__owner=request.user)
        return self.render_to_response({"module":module})
class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self,request):
        for id,order in self.request_json.items():
            Module.objects.filter(id=id,course__owner=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})
    pass
class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):

    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin,View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self,request,subject=None):
        subjects = Subject.objects.annotate(total_courses=(Count('courses')))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject,slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response({
            'subjects':subjects,
            'subject':subject,
            'courses':courses
            })
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context
    def post(self,request):
        return None

"""
    class OwnerCourseMixin(OwnerMixin):
        model = Course
        fields = ['subject', 'title', 'slug', 'overview']
        success_url = reverse_lazy('manage_course_list')
    class OwnerCourseEditMixin(OwnerCourseMixin,
    OwnerEditMixin):
        template_name = 'courses/manage/course/form.html'
    class ManageCourseListView(OwnerCourseMixin, ListView):
        template_name = 'courses/manage/course/list.html'
    class CourseCreateView(OwnerCourseEditMixin, CreateView):
        pass
    class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
        pass
    class CourseDeleteView(OwnerCourseMixin, DeleteView):
        template_name = 'courses/manage/course/delete.html'
"""
