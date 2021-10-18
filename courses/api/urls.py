from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework.authtoken import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('courses',CourseViewSet)

# user_router = routers.DefaultRouter(trailing_slash=False)
# user_router.register('users',UserViewSet)


app_name = 'api'
urlpatterns = [
    path('subjects',
            SubjectListView.as_view(),
            name='subject_list'
        ),
    path('subjects/<int:pk>',
            SubjectDetailView.as_view(),
            name='subject_detail'
        ),
    path('users/<int:pk>',
            UserDetailView.as_view(),
            name='user_detail'
        ),
    path('users/<int:pk>/update',
            UserUpdateView.as_view(),
            name='user_update'
        ),
    path('register',
            UserCreateView.as_view(),
            name = 'user_create'
        ),
    path('',include(router.urls)),
]
