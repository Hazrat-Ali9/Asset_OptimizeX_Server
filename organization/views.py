from django.shortcuts import render
from rest_framework.views import APIView
from organization.serializers import *
from account.renders import UserRenderer
from rest_framework.permissions import IsAuthenticated
from organization.models import Organization
from rest_framework import viewsets
from rest_framework.response import Response
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from account.utils import Util
from django.core.exceptions import ValidationError
from organization.models import Organization
from rest_framework import status


class OrganizationRegisterAPIView(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    queryset = Organization.objects.all()
    serializer_class = organigationRegisterSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      if serializer.is_valid():
        serializer.save(user = self.request.user)
        user = self.request.user
        print("EMail: ", user.id)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        organization_name =  serializer.data.get('organization_name')       
             
        link = "http://localhost:5173/api/organization/register/"
        print("uid", uid, " Token", token, " link", link, 'organizationName', organization_name)
        body = 'Click Following link to Active Your Account ' + link +  uid + '/'+ token + '/' + organization_name
        data = {
          'subject':'Active Your Account',
          'body':body,
          'to_email':user.email,
        }
        Util.send_email(data)
        # Return a custom response with a message and status code
        return Response({'message': 'Please Check Your Email'}, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
  
class registerOrganizationVerify(APIView):
  renderer_classes = [UserRenderer]
  def get(self, request, uid, token,organization_name, format = None):
    serializer = registerOrganizationVerifySerializer(data=request.data, context = {'uid':uid, 'token':token, 'organization_name':organization_name})
    if serializer.is_valid(raise_exception=True):
      
      return Response({
        'msg':'Organization Account Active Successfully'
      })
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
     


