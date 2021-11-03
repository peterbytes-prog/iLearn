from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('room/<int:course_id>/',
            course_chat_room,
            name = 'course_chat_room'
        )
]
