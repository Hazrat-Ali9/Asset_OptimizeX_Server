from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import uploadAsset,AssetVersion
from .serializers import uploadAssetSerializer,PreviousVersionSerializer,CurrentAssetSerializer,AssetVersionSerializer

class AssetListsCreateView(generics.ListCreateAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    
#for retrive data librarywise
class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the library_id from the URL parameter
        library_id = self.kwargs.get('library_id')

        if library_id is None:
            # Return a response with an error message if library_id is missing
            return Response({'error': 'Library ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = uploadAsset.objects.filter(library_id=library_id)
        return queryset
    

class AssetRetrieveView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]

class AssetUpdateView(generics.UpdateAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]

class AssetDeleteView(generics.DestroyAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]


#asset version control views.....

class PreviousAssetVersionsView(generics.ListAPIView):
    serializer_class = PreviousVersionSerializer

    def get_queryset(self):
        # Get the asset_id from the URL parameter
        asset_id = self.kwargs['asset_id']

        # Retrieve the asset instance
        try:
            asset_instance = uploadAsset.objects.get(id=asset_id)
        except uploadAsset.DoesNotExist:
            asset_instance = None

        # If the asset instance is found, return its previous versions
        if asset_instance:
            return asset_instance.versions.all()
        else:
            return AssetVersion.objects.none()
    
    # def get_queryset(self):
    #     asset_id = self.kwargs.get('asset_id')

    #     if asset_id is None:
    #         # Return a response with an error message if library_id is missing
    #         return Response({'error': 'assert_id ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     queryset = AssetVersion.objects.filter(id=asset_id)
    #     return queryset

class CurrentAssetView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = CurrentAssetSerializer        

class AssetVersionListView(generics.ListAPIView):
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer