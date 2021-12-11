from django.urls import path
from .views import *

app_name = 'students'

urlpatterns = [
    path('register/',
            StudentRegistrationView.as_view(),
            name = 'student_registration'
        ),
    path('enroll-course/',
            StudentEnrollCourseView.as_view(),
            name = 'student_enroll_course'
        ),
    path('courses/',
            StudentCourseListView.as_view(),
            name="student_course_list"
        ),
    path('course/<int:pk>/',
            StudentCourseDetailView.as_view(),
            name='student_course_detail'
        ),

    path("course/<int:pk>/<int:module_id>/",
            StudentCourseDetailView.as_view(),
            name='student_course_detail_module'
        ),
    path("course/<int:pk>/assignment/",
            StudentCourseAssignmentDetailView.as_view(),
            name='student_course_assignment_detail'
        ),
    path("course/<int:pk>/assignment/<int:assignment_id>/",
            StudentCourseAssignmentDetailView.as_view(),
            name='student_course_a_assignment_detail'
        ),


    path("course/drop/<int:pk>",
            StudentCourseDelete.as_view(),
            name='drop_course'
        )
]
