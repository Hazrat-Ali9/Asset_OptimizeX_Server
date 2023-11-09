

# serializers.py
from rest_framework import serializers
from .models import SharedAsset

class SharedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedAsset
        # fields = '__all__'
        # exclude = ('short_url',)
        fields = '__all__'