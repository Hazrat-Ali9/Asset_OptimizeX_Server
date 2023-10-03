from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import *

######### User Resistration Serializers ####################
class UserRegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
  
  class Meta:
    model = User
    fields = ['email', 'name', 'phone_number', 'password', 'password2']
    extra_kwargs = {
      'password':{'write_only':True},
      
    }
  
  ## Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2') 
   
    if len(password) < 8 or len(password2) < 8:
      raise serializers.ValidationError('Your password must contain at least 8 characters.')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")  
    return attrs      
    
 
  def create(self, validate_data):   
    return User.objects.create_user(**validate_data)
  
######### Register  Accout Active Serializer ############
# class RegisterAccountSerializer(serializers.Serializer):
  # def validate(self, attrs):
  #   uid = self.context.get('uid')
  #   token = self.context.get('token')
  #   id = smart_str(urlsafe_base64_decode(uid))
  #   user = User.objects.get(id = id)
  #   if user is not None:
  #     user.is_active = True
  #     user.save()
  #     return attrs
  #   else:
  #     raise ValidationError('Token is not Valid or Expired')
  
########## User Login Serializers #################
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
    
############ User Profile Serializer ################
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
  
################# User Profile Update Serilizer ##########
class UserProfileUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['name', 'bio', 'country', 'zip_code']  
  def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.name = validated_data['name']
        instance.bio = validated_data['bio']
        instance.country = validated_data['country']
        instance.zip_code = validated_data['zip_code']

        instance.save()
        return instance
    
  
####### user Change password Serializer #####
class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']
  
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    
    if len(password) < 8 or len(password2) < 8:
      raise serializers.ValidationError('Your password must contain at least 8 characters.')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs


########### Send Email Reset Password ####
class SendPasswordEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255) 
  class Meta:
    fields = ['email']
    
  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email= email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID ', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print("password Reset Token", token)
      link = "http://localhost:5173/api/user/reset/"+uid+'/'+token
      print('Password reset link', link)
      
      ## Send Email
      body = 'Click Following Link to Reset Your Password ' + link
      data = {
        'subject' :'Reset Your Password',
        'body': body,
        'to_email': user.email,
        
      }
      Util.send_email(data)
      return attrs         
    else:
      raise ValidationErr("You are not a Registered User")
      
########## user password reset serializer
class  UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2'] 
    
  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')  
      
      if len(password) < 8 or len(password2) < 8:
        raise serializers.ValidationError('Your password must contain at least 8 characters.')
      if password != password2:
        raise serializers.ValidationError("Password and confirm password doesn't match")
      id =smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id = id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise ValidationError('Token is not Valid or Expired')  
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise ValidationError("Token is not Valid or Expired")
    

  
   

  
  
  