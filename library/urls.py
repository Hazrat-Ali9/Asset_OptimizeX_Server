from django.urls import path
from .views import CreateLibraryAPIView, LibraryDetailAPIView, ListLibraryAPIView, assetAllImageView

urlpatterns = [
    path('create/', CreateLibraryAPIView.as_view(), name='create-library'),
    path('<int:pk>/', LibraryDetailAPIView.as_view(), name='library-detail'),
    path('list/<int:org_id>/', ListLibraryAPIView.as_view(), name='list-library-by-org'),
    ####### All Asset showing Organization ##########
    path('asset/<int:org_id>/', assetAllImageView.as_view(), name = 'org_asset_all')
]
