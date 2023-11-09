from organization.models import *
from rest_framework import serializers
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator


########### addMember Serializer ######
class addMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField(max_length=100)
    organization = serializers.CharField(max_length=100)
    class Meta:
        fields = ['email', 'role', 'organization']
        
########### addMember Serializer ######
class InvitedaddMemberSerializer(serializers.Serializer):
    organization_name = serializers.CharField(max_length=150)
    invited_code = serializers.IntegerField()
    class Meta:
        fields = ['organization_name', 'invited_code']

############ Organization Register Serializer ##################
class organigationRegisterSerializer(serializers.ModelSerializer):
    member = addMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = '__all__'
   
############# Active Register Organization ###############     
class registerOrganizationVerifySerializer(serializers.Serializer):
    def validate(self, attrs):
        uid = self.context.get('uid')
        token = self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id = id)
        organization_name = self.context.get('organization_name')
        org_name = smart_str(urlsafe_base64_decode(organization_name))
        org_code = 1
        for i in range(len(org_name)):
          org_code += ord(org_name[i])
        
        organization = Organization.objects.get(organization_name=org_name)
        if organization is None:
          raise ValidationError('You are not a Register Organization')
        if user is not None:
            organization.invited_code = org_code*3
            organization.is_company = True
            organization.save()
            user.save()
            return attrs
        else:
            raise ValidationError('Token is not Valid or Expired')
        

####### Member Active Serializer #######
class memberInvitedAcceptSerializer(serializers.Serializer):
  def validate(self, attrs):
    uid = self.context.get('uid')
    token = self.context.get('token')
    org_name = self.context.get('org_name')
   
    id = smart_str(urlsafe_base64_decode(uid))
    org_name = smart_str(urlsafe_base64_decode(org_name))
    user = User.objects.get(id = id)
    org = Organization.objects.get(organization_name = org_name)  
    token = default_token_generator.check_token(user, token)
    add = addMember.objects.filter(organization=org)
    
    if user is not None:
      for i in add:
        print(i.email)
        if i.user == user:
          i.is_company = True
          user.save()
          i.save()
          return attrs
    else:
      raise ValidationError('Token is not Valid or Expired')

####### Organization Update Serializer ######
class organizationUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = ['organization_name', 'description', 'organization_logo', 'country', 'zip_code', 'company_phone_number']

####### Member Permission Update Serializers ########
class MemberPermissionUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = addMember
    fields = ['role']

