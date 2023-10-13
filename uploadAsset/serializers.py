from rest_framework import serializers
from .models import uploadAsset,AssetVersion
        
class uploadAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadAsset
        fields = ['id', 'organization', 'title', 'library', 'description', 'asset', 'location']
        
            

class PreviousVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetVersion
        fields = ('id','asset', 'created_at')  # Define the fields you want to include in the response

class CurrentAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadAsset
        fields = ('id', 'asset', 'created_at') 
     
#all asset        
class AssetVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetVersion
        fields = ('id', 'title', 'asset', 'created_at')         