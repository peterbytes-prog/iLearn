from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from students.views import StudentCourseDetailMixin
from django.views.generic.detail import DetailView


class CourseChatRoomView(StudentCourseDetailMixin,  DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['page'] = 'chat'
        return context

# @login_required
# def course_chat_room(request, course_id):
#     try:
#         enrollment = request.user.student.enrollments.get(course__pk=course_id)
#     except:
#         return HttpResponseForbidden()
#     return render(request, 'chat/room.html', {'course':enrollment.course})
