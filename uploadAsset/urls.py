from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'video', views.FileViewSet)

urlpatterns = [
    #libraywise data retrieve
    # path('', include(router.urls)),
    path('libraries/<int:library_id>/assets/', views.AssetListCreateView.as_view(), name='library-assets'),

    # List all assets or create a new asset
    path('assets/', views.AssetListsCreateView.as_view(), name='asset-list-create'),

    # Retrieve a specific asset
    path('assets/<int:pk>/', views.AssetRetrieveView.as_view(), name='asset-retrieve'),

    # Update a specific asset
    path('assets/<int:pk>/update/', views.AssetUpdateView.as_view(), name='asset-update'),

    # Delete a specific asset
    path('assets/<int:pk>/delete/', views.AssetDeleteView.as_view(), name='asset-delete'),
    
    #AssetVersion
     path('asset-versions/', views.AssetVersionListView.as_view(), name='asset-versions-list'),
     path('assets/prev/<int:asset_id>/', views.PreviousAssetVersionsView.as_view(), name='previous-asset-versions'),
     path('assets/current/<int:pk>/', views.CurrentAssetView.as_view(), name='current-asset'),
     
     ## asset Download ##
     path('download/<int:id>/', views.FileDownloadAPIView.as_view()),
     path('search/image/<int:pk>/', views.ImageFilter.as_view()),
     path('search/audio/<int:pk>/', views.AudioFilter.as_view()),
     path('search/video/<int:pk>/', views.VideoFilter.as_view()),
]