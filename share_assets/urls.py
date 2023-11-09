# urls.py in the "shareassets" app
from django.urls import path
from . import views

urlpatterns = [
    path('asset/', views.ShareAssetView.as_view(), name='share-asset'),
    path('<str:short_url>/', views.RetrieveSharedAssetView.as_view(), name='retrieve-shared-asset'),
]