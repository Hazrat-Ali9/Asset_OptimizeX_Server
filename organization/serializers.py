from organization.models import Organization
from rest_framework import serializers
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

############ Register Serializer ##################
class organigationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['organization_name',  'description', 'country', 'zip_code', 'tc', 'company_phone_number']
   
############# Active Register Organization ###############     
class registerOrganizationVerifySerializer(serializers.Serializer):
    def validate(self, attrs):
        uid = self.context.get('uid')
        token = self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id = id)
        organization_name = self.context.get('organization_name')
        org_name = smart_str(urlsafe_base64_decode(organization_name))
        
        organization = Organization.objects.get(organization_name=org_name)
        if organization is None:
          raise ValidationError('You are not a Register Organization')
        if user is not None:
            organization.is_company = True
            organization.save()
            user.save()
            return attrs
        else:
            raise ValidationError('Token is not Valid or Expired')


class totalOrganization(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['organization_name', 'organization_logo', 'description', 'country', 'zip_code', 'tc', 'company_phone_number']
        


