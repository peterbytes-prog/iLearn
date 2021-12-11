from rest_framework.permissions import BasePermission
from students.models import Student
class IsEnrolled(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.course_enrollements.filter(student__user__in=[request.user])
class IsOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        return request.user.pk == obj.pk
