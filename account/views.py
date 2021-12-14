from django.shortcuts import render
from django.urls import reverse
from .forms import (UserEditForm, StudentEditForm)
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from students.models import Student


class ProfileDetailView(FormMixin,  DetailView):
    model = Student
    form_class = StudentEditForm
    template_name = 'account/profile_detail.html'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        if (self.object.user == self.request.user):
            context['student_form'] = StudentEditForm(instance=self.object)
            context['user_form'] = UserEditForm(instance=self.object.user)
        return context
    def get_success_url(self):
        return reverse('profile:profile-detail',  kwargs={'pk': self.object.pk})

    def post(self,  request,  *args,  **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        if self.object.user!=request.user:
            return HttpResponseForbidden()
        form = self.get_form()#not ready needed
        student_form = StudentEditForm(instance=self.object, data=request.POST, files=request.FILES)
        user_form = UserEditForm(instance=self.object.user, data=request.POST)

        if student_form.is_valid() and user_form.is_valid():
            student_form.save()
            user_form.save()
            return self.form_valid(form)#let form_valid handle it
        else:
            return self.form_invalid(form)
