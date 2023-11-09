from rest_framework import serializers
from .models import uploadAsset,AssetVersion
from django.core.files import File
import base64

class updateUploadSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()
    class Meta:
        model = uploadAsset
        fields = ['id', 'organization', 'title', 'library', 'description', 'base64_image', 'location']
        
    def get_base64_image(self, obj):
        f = open(obj.image_file.path, 'rb')
        image = file(f)
        data = base64.b64encode(image.read())
        f.close()
        return data
        
class uploadAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadAsset
        fields = ['id', 'organization', 'title', 'library', 'description', 'asset', 'location']

#### Download Asset Serializers ###
class AssetSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj):
        return obj.get_download_url()

    class Meta:
        model = uploadAsset
        fields = ['id', 'title', 'download_url']

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
        
        

# class FileSerializer(serializers.ModelSerializer):
#     file = FileTypeField(allowed_types=['video/mp4', 'audio/mpeg', 'image/png'])

#     class Meta:
#         model = uploadAsset
#         fields = ['asset']              