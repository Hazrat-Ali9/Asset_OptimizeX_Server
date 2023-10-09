# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import SharedAsset
from .serializers import SharedAssetSerializer
from django.shortcuts import get_object_or_404
from uploadAsset.models import uploadAsset
from uploadAsset.serializers import uploadAssetSerializer
from django.utils import timezone
from django.http import Http404

class ShareAssetView(generics.CreateAPIView):
    queryset = SharedAsset.objects.all()
    serializer_class = SharedAssetSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Extract expiration duration from request data
        expiration_duration = request.data.get('expiration_duration')
        if not expiration_duration:
            return Response({'error': 'Expiration duration is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create a shared asset entry
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, expiration_duration=expiration_duration)

        # Retrieve the serialized data, including the short_url
        shared_asset_data = serializer.data

        return Response(shared_asset_data, status=status.HTTP_201_CREATED)


class RetrieveSharedAssetView(generics.RetrieveAPIView):
    queryset = SharedAsset.objects.all()
    serializer_class = uploadAssetSerializer  # Use the serializer for uploadAsset

    def retrieve(self, request, short_url, *args, **kwargs):
        try:
            # Retrieve the shared asset based on the provided short_url
            shared_asset = SharedAsset.objects.get(short_url=short_url)
            
            # Check if the link has expired
            if shared_asset.created_at + timezone.timedelta(seconds=shared_asset.expiration_duration) < timezone.now():
                return Response({'error': 'The link has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the associated uploadAsset
            asset = shared_asset.asset
            serializer = uploadAssetSerializer(asset)
            return Response(serializer.data)
        except SharedAsset.DoesNotExist:
            raise Http404