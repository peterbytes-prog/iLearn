from rest_framework import serializers

from ..models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from students.models import Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name']
    pass
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'order',
            'title',
            'description'
        ]
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','title','slug']
class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    students = UserSerializer(many=True,read_only=True)
    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "students",
            "modules"
        ]

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self,value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order','item']
class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order','title','description','contents']

class CourseWithModuleContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    owner = UserSerializer(read_only=True)
    students = UserSerializer(read_only=True,many=True)
    class Meta:
        model = Course
        fields = ['id',
                'subject',
                'title',
                'slug',
                'overview',
                'created',
                'owner',
                "students",
                'modules'
                    ]
class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id',
                    "username",
                    'password',
                    "email",
                    "first_name",
                    "last_name",
                    ]
    def create(self,validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
