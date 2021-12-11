from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('room/<int:pk>/',
            CourseChatRoomView.as_view(),
            name = 'course_chat_room'
        )
]
