from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()

# router.register("asset", views.ProductsViewSet)


urlpatterns = [
    # path("", include(router.urls)),
    
    #libraywise data retrieve
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
    # Delete AssetsVersion by calling by there AssetsVersion PK
     path('assets/delete/<int:pk>/', views.AssetVersionDeleteView.as_view(), name='asset-version-delete'),
]