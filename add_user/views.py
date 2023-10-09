from django.shortcuts import render
from rest_framework import views,  permissions,response,status, viewsets, generics
from add_user.serializers import *
from account.renders import UserRenderer
from account.utils import Util
from add_user.models import addUser
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from organization.models import Organization
from account.utils import Util
# Create your views here.
from account.models import User

########## Add Member Organization #############
class AddMemberView(generics.CreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  queryset = addUser.objects.all()
  serializer_class = addMemberSerializer

  def create(self, request, *args, **kwargs):
    email = request.data.get('email')
    permission = request.data.get('permission')
    organization_name = request.data.get('organization')
    print(organization_name)
    if request.user.email == email:
      return response.Response("Not Valid Email!")
    try:
      organization = Organization.objects.get(organization_name=organization_name) ## Check Organization Register or Available
      
      try:
        already_addedEmail = addUser.objects.get(organization=organization)
        if already_addedEmail.email == email:
          return response.Response('Email Already Added', status=status.HTTP_405_METHOD_NOT_ALLOWED)
      except addUser.DoesNotExist:
        try:   
          user = User.objects.get(email=email) #### Check Our Website User Register  

          id = user.id
          uid = urlsafe_base64_encode(force_bytes(id))
          token = default_token_generator.make_token(user)
          org_name = urlsafe_base64_encode(force_bytes(email))

          user = addUser.objects.create(organization=organization, email=email, permission=permission, is_addUser=False, is_company=False)
          
          link = 'http://127.0.0.1:8000/api/add-user/add/'
          body = "Invited Request Accept Click This Link " + link + uid +'/' + token + '/' +org_name
          data ={
            'subject':'Company membership invite request',
            'body': body,
            'to_email': email,
          }
          Util.send_email(data)
          serializer = addMemberSerializer(user)
          # serializer.is_valid(raise_exception=True)
          # serializer.save()
          return response.Response({'message':'Invited Email Request Send.'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
          return response.Response({'message':"User Not Register"}, status=status.HTTP_404_NOT_FOUND)
    except Organization.DoesNotExist:
            return response.Response({'message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
class requestAccept(views.APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, uid, token,org_name, format= None):
    serializer = requestAcceptSerializer(data= request.data, context = {'uid':uid, 'token':token, 'org_name':org_name})
    if serializer.is_valid(raise_exception=True):
      return response.Response({
        'msg':'Add User Account Active Successfully'
      })
    print("ALU")
    return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)