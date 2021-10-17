from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register('courses',CourseViewSet)


app_name = 'api'
urlpatterns = [
    path('subjects/',
            SubjectListView.as_view(),
            name='subject_list'
        ),
    path('subjects/<pk>/',
            SubjectDetailView.as_view(),
            name='subject_detail'
        ),
    path('',include(router.urls)),
]
