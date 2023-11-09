from django.urls import path, include
from feedback.views import *



urlpatterns = [
     path('feedback/', FeedbackView.as_view()),
     path('feedback-show/', ShowFeedBackView.as_view()),
]

