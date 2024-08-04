"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path

from users.views import (
    EmailExistsAPIView,
    UsernameExistsAPIView,
    RegistrationStepOneAPIView,
    RegistrationStepTwoAPIView,
    RegistrationStepThreeAPIView,
    LoginAPIView,
    UserDetailsAPIView,
    LogoutAPIView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rendering.urls')),
    re_path(r'^api/(email-exists|login/email-exists|register/email-exists)/$', EmailExistsAPIView.as_view(), name='email-exists'),
    re_path(r'^api/(username-exists|login/username-exists)/$', UsernameExistsAPIView.as_view(), name='username-exists'),
    re_path(r'^api/(?:login-user|login/login-user)/$', LoginAPIView.as_view(), name='login-user'),
    re_path(r'^api/(?:logout-user|logout/logout-user)/$', LogoutAPIView.as_view(), name='logout-user'),
    re_path(r'^api/(?:register-step-one|register/register-step-one)/$', RegistrationStepOneAPIView.as_view(), name='register-step-one'),
    re_path(r'^api/(?:register-step-two|register/register-step-two)/$', RegistrationStepTwoAPIView.as_view(), name='register-step-two'),
    re_path(r'^api/(?:register-step-three|register/register-step-three)/$', RegistrationStepThreeAPIView.as_view(), name='register-step-three'),
    path('api/get-user-details/', UserDetailsAPIView.as_view(), name='get-user-details'),
]
