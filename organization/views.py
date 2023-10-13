from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import (generics, permissions, response, status, views,
                            viewsets)

from account.models import User
from account.renders import UserRenderer
from account.utils import Util
from organization.models import *
from organization.serializers import *


############## Register Organization #################
class OrganizationRegisterView(viewsets.ModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  queryset = Organization.objects.all()
  serializer_class = organigationRegisterSerializer
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data = request.data)
    if serializer.is_valid():
      serializer.save(owner = self.request.user)
      user = self.request.user
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = default_token_generator.make_token(user)
      organization_name =  serializer.data.get('organization_name')    
      organization_name = urlsafe_base64_encode(force_bytes(organization_name))   
            
      link = "http://localhost:5173/api/organization/register/"
      print("uid", uid, " Token", token, " link", link, 'organizationName', organization_name)
      body = 'Click Following link to Active Your Account ' + link +  uid + '/'+ token + '/' + organization_name
      data = {
        'subject':'Active Your Account',
        'body':body,
        'to_email':user.email,
      }
      Util.send_email(data)

      return response.Response({'message':'Check mail Active Your Organization'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
############## Active Organization ##################
class registerOrganizationVerify(views.APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token,organization_name, format = None):
    serializer = registerOrganizationVerifySerializer(data=request.data, context = {'uid':uid, 'token':token, 'organization_name':organization_name})
    if serializer.is_valid(raise_exception=True):

      return response.Response({
        'message':'Organization Account Active Successfully'
      })
    return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
          
 
############ Organization Get ##########
class OrganizationTotal(views.APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            owner_organization = Organization.objects.filter(owner=request.user)
            owner_organization_data = []
            for i in owner_organization:
              if i.is_company == True:
                dic = {}
                dic['id'] = i.id
                dic['organization_name'] = i.organization_name
                owner_organization_data.append(dic)
                 
            member_organizations = Organization.objects.filter(member=request.user)
            member_organization_data = []
            for i in member_organizations:
              if i.is_company == True:
                dic = {}
                dic['id'] = i.id
                dic['organization_name'] = i.organization_name
                member_organization_data.append(dic)
            
            return response.Response({
                'owner_organizations': owner_organization_data,
                'member_organizations': member_organization_data},status=status.HTTP_200_OK
            )

        except Organization.DoesNotExist:
            return response.Response({'message': 'No organizations found'}, status=status.HTTP_404_NOT_FOUND)
          
########### Organization Member Request View #######
class addMemberView(views.APIView):
  permission_classes= [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  def post(self, request):
    serializer = addMemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    role = serializer.data.get('role')
    organization_name = serializer.data.get('organization')
    
    try:
      user = User.objects.get(email=email)
      if request.user == user:
        return response.Response("Not Valid Email")
      try:
        organization = Organization.objects.get(organization_name=organization_name)
        if organization.owner != request.user:
          return response.Response({
            "msg":"Your are not access this organization add user option"
          })
        th = organization.member.all()
        for i in th:
          if i.email == email:
            return response.Response("This user Already added")       
        member = addMember.objects.create(user=user, organization=organization, email=email, role=role, is_company=False)
        member.save()
        organization.save()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        org_name = urlsafe_base64_encode(force_bytes(organization_name))
        link = "http://localhost:5173/api/organization/add-user/"
        print("uid", uid, " Token", token, " link", link)
        body = 'Click Following link to confirm invited accepted ' + link +  uid + '/'+ token + '/' + org_name
        data = {
          'subject':'Invited Request',
          'body':body,
          'to_email':email,
        }
        Util.send_email(data)
        
        return response.Response({'message':"Invited Link send."})
        
      except Organization.DoesNotExist:
        return response.Response({'msg':"Organization not register"})
    except User.DoesNotExist:
      return response.Response({"msg":"user not register"})

# class addMemberView(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     renderer_classes = [UserRenderer]
#     queryset = addMember.objects.all()
#     serializer_class = addMemberSerializer
    
#     def create(self, request, *args, **kwargs):
#       serializer = self.get_serializer(data=request.data)
#       serializer.is_valid(raise_exception=True)
       
#       # user = request.data.get('user')
#       role = request.data.get('role')
#       organization = request.data.get('organization')
#       email = request.data.get('email')
#       s = User.objects.get(email=email) 
#       iii = Organization.objects.filter(member=s)
#       print(iii)
#       try:
#         us = User.objects.get(email=email)        
#         if us == request.user:
#           return response.Response("Email not Valid")
#         else:
#           try:
#             already_added = Organization.objects.get(member=us)
#             print(already_added)
#             return response.Response("Alread added This User")
#           except Organization.DoesNotExist: 
#             serializer.save()
#             uid = urlsafe_base64_encode(force_bytes(us.id))
#             token =default_token_generator.make_token(us)
#             org_id = urlsafe_base64_encode(force_bytes(organization))
#             print(uid)
#             link = "http://localhost:5173/api/organization/add-user/"
#             print("uid", uid, " Token", token, " link", link)
#             body = 'Click Following link to confirm invited accepted ' + link +  uid + '/'+ token + '/' + org_id
#             data = {
#               'subject':'Invited Request',
#               'body':body,
#               'to_email':us.email,
#             }
#             Util.send_email(data)
            
#             return response.Response({'message':"Invited Link send. Check Email"})
            
#       except User.DoesNotExist:
#         return response.Response({'message': "Not Register User"})
        
         
#  ############## Active Organization ##################

class invitedActive(views.APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token,org_name, format = None):
    serializer = memberInvitedAcceptSerializer(data=request.data, context = {'uid':uid, 'token':token, 'org_name':org_name})
    if serializer.is_valid(raise_exception=True):
      
      return response.Response({
        'massage':'Invited request Confirm Successfully'
      })
    return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    
      