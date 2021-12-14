from django.urls import path, include
from .views import (CourseAssignmentListDetailView,
        CourseAssignmentListUpdateView,
        CourseAssignmentListUpdateView,
        QuestionCreateUpdateDetailView,
        StudentTestPage,
        StudentTestReviewPage, 
    )

app_name = 'assignments'
urlpatterns = [
    path('', CourseAssignmentListDetailView.as_view(), name='course_assignment_question_list'),
    path('<int:assignment_id>', CourseAssignmentListDetailView.as_view(), name='course_a_assignment_question_list'),
    path('update', CourseAssignmentListUpdateView.as_view(), name='course_assignment_update'),
    path('<int:assignment_id>/question/create/',
            QuestionCreateUpdateDetailView.as_view(),
            name ='assignment_question_create'
        ),
    path('<int:assignment_id>/question/<int:question_id>/edit',
            QuestionCreateUpdateDetailView.as_view(),
            name ='assignment_question_update'
        ),
    path('<int:pk>/test',
        StudentTestPage.as_view(),
        name ='test_page'
        ),
    path('<int:assignment_id>/review/<int:pk>',
        StudentTestReviewPage.as_view(),
        name ='test_review_page'
        )
]

# urlpatterns = [
#     # path('',
#     #     CourseAssignmentListDetailView.as_view(),
#     #     name='course_assignment_question_list'),
#     path('manage',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/create',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/edit',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/delete',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/test',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/review',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#
#
#     path('manage/<int:assignment_id>/question/create',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/question/<int:question_id>/edit',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#     path('manage/<int:assignment_id>/question/<int:question_id>/delete',
#         CourseAssignmentListDetailView.as_view(),
#         name='course_assignment_question_list'),
#
# ]
