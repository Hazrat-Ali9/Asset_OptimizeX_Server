from rest_framework import serializers

from library.models import Library
from organization.models import Organization


class CreateLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['library_name', 'description', 'organization']
        
    def validate(self, attrs):
        library_name = attrs.get('library_name')
        description = attrs.get('description')
        organization = attrs.get('organization')
        try:
            dup = Library.objects.filter(organization=organization)     
            for i in dup:     
                if library_name == i.library_name:
                    raise serializers.ValidationError("This library name already create")
                return attrs
        except Library.DoesNotExist:
            return attrs