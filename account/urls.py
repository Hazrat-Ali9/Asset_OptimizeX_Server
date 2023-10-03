from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from account.views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    # path('register/<uid>/<token>/', RegisterAccountActivate.as_view(), name = 'active-account'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('profile-update/<int:pk>/', UserUpdateProfileView.as_view(), name = 'profile-update'),
 
    path('changepassword/', 
         UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name = 'send-reset-password-email'), 
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name = 'reset-password'),
   
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
