from django.urls import path
from library.views import *

urlpatterns = [
    path('create/', CreateLibraryAPIView.as_view(), name='create-library'),
    ### Library Update Url ####
    path('update/<int:pk>/', LibraryUpdateView.as_view(), name='library-detail'),
    #### Library Delete Url ####
    path('delete/<int:pk>/', LibraryDeleteView.as_view(), name='library-detail'),
    
    path('list/<int:org_id>/', ListLibraryAPIView.as_view(), name='list-library-by-org'),
    ####### All Asset showing Organization ##########
    path('asset/<int:org_id>/', assetAllImageView.as_view(), name = 'org_asset_all'),
    
    # path('show/<int:pk>/', assetAlleImageView.as_view()),
]
