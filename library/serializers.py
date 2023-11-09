from rest_framework import serializers

from library.models import Library
from organization.models import *

class CreateLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['library_name', 'description', 'organization']
        
    def validate(self, attrs):
        library_name = attrs.get('library_name')
        description = attrs.get('description')
        organization = attrs.get('organization')  
        user = self.context.get('user') 
        member = addMember.objects.filter(organization=organization)
        
        for i in member:
            if i.user == user:
                if i.role == 'Admin' or i.role == 'Contributor':
                    break
                else:
                    raise serializers.ValidationError("You don't have permission to Create Library.") 
                    return attrs       
        try:
            org = Organization.objects.get(organization_name=organization) 
            dup = Library.objects.filter(organization=org)   
            if len(dup) >= 2 and org.premiumUser == False:
                raise serializers.ValidationError("Your Organization has exceeded the number of Library limit and you must purchase Premium to add additional Library.")
                   
            for i in dup:
                if i.library_name == library_name:
                    raise serializers.ValidationError("This library name already create")
                    return attrs
            return attrs
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization Didn't find")
 
                            
     