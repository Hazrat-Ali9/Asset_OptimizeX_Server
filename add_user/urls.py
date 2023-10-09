from django.urls import path, include
from rest_framework.routers import DefaultRouter
from add_user.views import *



urlpatterns = [
    path('add/', AddMemberView.as_view()),
    path('add/<uid>/<token>/<org_name>/', requestAccept.as_view()),
]
