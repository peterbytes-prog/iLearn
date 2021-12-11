from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject,Course,Enrollment
from django.shortcuts import get_object_or_404
from .serializers import (SubjectSerializer,
                            CourseSerializer,
                            CourseWithModuleContentsSerializer,
                            UserDetailSerializer)
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsEnrolled,IsOwner
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    @action(detail=True,
            methods=['post'],
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        self.course_enrollement = Enrollment.objects.get_or_create(student=request.user.student,course=course)
        return Response({"enrolled":True})
    @action(detail=True,
            methods=['get'],
            serializer_class = CourseWithModuleContentsSerializer,
            authentication_classes = [TokenAuthentication],
            permission_classes = [IsAuthenticated,IsEnrolled])
    def contents(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    #unenroll
    @action(detail=True,
            methods=['post'],
            serializer_class = CourseWithModuleContentsSerializer,
            authentication_classes = [TokenAuthentication],
            permission_classes = [IsAuthenticated,IsEnrolled])
    def drop(self,request,*args,**kwargs):
        course = self.get_object()
        enroll = Enrollment.objects.filter(course=course,student = request.user.student)
        if enroll:
            enroll.delete()
        return Response({"enrolled":False})

class UserMixin(object):
    """docstring for ."""
    model = User
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class UserDetailView(UserMixin,generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,IsOwner]
    authentication_classes = [TokenAuthentication]

class UserUpdateView(UserMixin,generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,IsOwner]
    authentication_classes = [TokenAuthentication]

class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserDetailSerializer
    permission_classes=[AllowAny]
    authentication_classes = []


#
