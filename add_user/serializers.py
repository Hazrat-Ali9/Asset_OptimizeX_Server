from add_user.models import addUser
from rest_framework import serializers
from organization.models import Organization
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from organization.models import Organization
from account.models import User

class addMemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = addUser
    fields = ['email','permission', 'organization']
    

class requestAcceptSerializer(serializers.Serializer):
  def validate(self, attrs):
    uid = self.context.get('uid')
    token = self.context.get('token')
    org_name = self.context.get('org_name')
    
    id = smart_str(urlsafe_base64_decode(uid))
    org_name = smart_str(urlsafe_base64_decode(org_name))
    user = User.objects.get(id = id)
    # user = Organization.objects.get(organization_name=org_nami)  
    token = default_token_generator.check_token(user, token)
    add = addUser.objects.get(email=org_name)
    
    print(add.email, org_name)
    if user is not None:
      add.is_company = True
      add.is_addUser = True
      user.save()
      add.save()
      return attrs
    else:
      raise ValidationError('Token is not Valid or Expired')

    