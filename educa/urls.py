"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from courses.views import CourseListView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as token_views
import os

urlpatterns = [
    # path('accounts/login/',auth_view.LoginView.as_view(),name='login'),
    # path('accounts/logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('',CourseListView.as_view(),name='course_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('account.urls',namespace='profile')),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls',namespace='courses')),
    path('students/',include('students.urls',namespace='students')),
    path('api/',include('courses.api.urls',namespace='api')),
    path('api-token-auth/',token_views.obtain_auth_token),
    path('chat/',include('chat.urls',namespace='chat')),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
