from django.urls import path, include
from organization.views import *

urlpatterns = [
  path('register/', OrganizationRegisterAPIView.as_view()),
  path('register/<uid>/<token>/<organization_name>/', registerOrganizationVerify.as_view()),
  path('list/', OrganizationTotal.as_view()),
]
