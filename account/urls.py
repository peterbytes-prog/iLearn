from django.urls import path
from .views import *


app_name = 'profile'

urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail')
    ]
