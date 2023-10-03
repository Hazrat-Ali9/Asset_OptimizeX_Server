from organization.models import Organization
from rest_framework import serializers
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

class organigationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['organization_name', 'description', 'country', 'zip_code', 'tc', 'company_phone_number']
        
class registerOrganizationVerifySerializer(serializers.Serializer):
    def validate(self, attrs):
        uid = self.context.get('uid')
        token = self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id = id)
        organization_name = self.context.get('organization_name')
        
        organization = Organization.objects.get(organization_name=organization_name)

        if user is not None:
            organization.is_company = True
            organization.save()
            user.save()
            return attrs
        else:
            raise ValidationError('Token is not Valid or Expired')
