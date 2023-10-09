from rest_framework import serializers

from library.models import Library
from organization.models import Organization


class CreateLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['library_name', 'description', 'organization']
        
    