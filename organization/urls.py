from django.urls import path, include
from organization.views import *
from rest_framework.routers import DefaultRouter
# from organization.demo import *
router = DefaultRouter()
router.register(r'register', OrganizationRegisterAPIView)


urlpatterns = [
  path('', include(router.urls)),
  path('register/<uid>/<token>/<organization_name>/', registerOrganizationVerify.as_view()),
]
