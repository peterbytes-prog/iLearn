from rest_framework.permissions import BasePermission
class IsEnrolled(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.students.filter(id=request.user.id).exists()
class IsOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        return request.user.pk == obj.pk
