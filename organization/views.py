from django.shortcuts import render
from organization.serializers import *
from account.renders import UserRenderer
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from account.utils import Util
from organization.models import *
from rest_framework import status, generics, views, viewsets, permissions, response
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from organization.ssl import sslcommerz_payment_gateway
import random

######### payment Gateway method ###########
@method_decorator(csrf_exempt, name='dispatch')
class successView(views.APIView):
  # permission_classes = [permissions.IsAuthenticated]
  def post(self, request):
    # user_id = request.user
    data = request.data
    user_id = int(data['value_b'])
    org_id = int(data['value_c'])
    amount = int(data['value_d'])
    user = User.objects.get(pk=user_id)
    org = Organization.objects.get(pk = org_id)
    
    payment = Payment.objects.create(
        user = user,
        organization=org,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid= amount,
        status =data['status'],
    )
    payment.save()
    
    order = Order.objects.get(user=user, is_ordered=False, order_number=int(data['value_a']))
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    org = Organization.objects.get(id= org_id)
    user = User.objects.get(id = user_id)
    premium = premiumOrder()
    premium.organization = org
    premium.payment = payment
    premium.user = user 
    premium.ordered = True
    premium.save()
    org.premiumUser = True
    org.save()
    
    return HttpResponseRedirect(redirect_to='http://localhost:5173/app/payment-success/')

########## Permium button Click Success View #########
class PlaceOrderPremiumView(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def post(self, request, pk):
    user = request.user
    try:
      org = Organization.objects.get(pk=pk)
      member = addMember.objects.filter(organization=org)
      for i in member:
        if i.user == self.request.user:
          if i.role == 'Contributor' or i.role == 'Viewer':
            return response.Response({'message': "You don't have permission to Payment method."})
      if org.premiumUser == True:
        return response.Response("Already You are Premium User")
      order = Order.objects.create(user=request.user, organization=org, is_ordered= False)

      order.order_number = order.id
      # sslcommerz_payment_gateway(request,order.id, pk, request.user.id)
      lst = {}
      lst['order_id'] = order.id 
      lst['org_id'] = pk
      lst['user_id'] = request.user.id
      lst['amount'] = 1000
      order.save()
      payment_url = sslcommerz_payment_gateway(request,request.user.name, order.id, pk, request.user.id, 1000)
      return response.Response(payment_url)
    except Organization.DoesNotExist:
      return response.Response('Organization Error')      
  
###### SSL Commerce Fail View #####
class PaymentFailView(views.APIView):
  # permission_classes = [permissions.IsAuthenticated]
  def post(self, request):
    return HttpResponseRedirect(redirect_to='http://localhost:5173/app/payment-failed/')
    
  
     
######### Payment History For Organization #######
class PaymentHistoryView(views.APIView):
  # permission_classes = [permissions.IsAuthenticated]
  
  def get(self, request, pk):
    try:
      org = Organization.objects.get(pk = pk)
      payment = Payment.objects.filter(organization=org)
      lst = []
      
      for i in payment:
        dic = {}
        dic['user'] = i.user.name
        dic['organization_name'] = i.organization.organization_name
        dic['payment_id'] = i.payment_id
        dic['payment_method'] = i.payment_method
        dic['amount'] = i.amount_paid
        dic['status'] = i.status
        dic['created_at'] = i.created_at
        lst.append(dic)
    
      return response.Response(lst, status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
      return response.Response('Information not Valid')
    
   
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
      
      org_name = urlsafe_base64_encode(force_bytes(organization_name))   
      
      
      link = "http://localhost:5173/api/organization/register/"
      print("uid", uid, " Token", token, " link", link, 'organizationName', organization_name)
      body = f'''Hi {user.name}

Please click on below link to confirm your Ogranization registration.''' + link +  uid + '/'+ token + '/' + org_name
      data = {
        'subject':f'Confirm your Organization account on {organization_name}',
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
          
############## Organization Update  View ###############
class organizationUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organization.objects.all()
    serializer_class = organizationUpdateSerializer
    
    def perform_update(self, serializer):
      pk = self.kwargs.get('pk')
      org = Organization.objects.get(pk = pk)
      member = addMember.objects.filter(organization=org)
      print(self.request.user)
      for i in member:
        if i.user == self.request.user:
          print(i.user)
          return response.Response({"message" : "You don't have permission to Organization Update."})
      print("ue")
      serializer.save()
      return response.Response({'message':"Successfully Updated."})
    
 
######### Organization Detail  View ###############
class organizationDetailView(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def get(self, request, pk):
    org = Organization.objects.get(pk=pk)
    lst = {}
    # lst['owner'] = org.owner
    lst['organization_name'] = org.organization_name
    # lst['organization_logo'] = org.organization_logo.url
    lst['description'] = org.description
    lst['country'] = org.country
    lst['zip_code'] = org.zip_code
    lst['org_phone_number'] = org.company_phone_number
    lst['created_date'] = org.created_date
    lst['invited_code'] = org.invited_code
    
    return response.Response(lst, status=status.HTTP_200_OK)
 
############## Organization Delete  View ###############
class organizationDeleteView(generics.DestroyAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = Organization.objects.all()
  serializer_class = organigationRegisterSerializer
  
  def destroy(self, request, *args, **kwargs):
    pk = self.kwargs.get('pk')
    org = Organization.objects.get(pk = pk)
    member = addMember.objects.filter(organization=org)
    for i in member:
      if i.user == self.request.user:
        return response.Response({'message':"You don't have permission to Delete Organization."})
    org.delete()
    return response.Response({'message':"Successfully Delete."})
    

############ Organization Get Total ##########
class OrganizationTotal(views.APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):   
      owner_organization = Organization.objects.filter(owner=request.user)
      owner_organization_data = []
      for i in owner_organization:
        if i.is_company == True:
          dic = {}
          dic['id'] = i.id
          dic['organization_name'] = i.organization_name
          dic['premiumUser'] = i.premiumUser
          owner_organization_data.append(dic)
          
      member_organization_data = []     
      member_organizations = addMember.objects.filter(user =request.user)
      print(member_organizations)
      for i in member_organizations:
        org = Organization.objects.filter(id = i.organization_id)
        dic = {}
        if i.is_company == True:
          dic['role'] = i.role
          for j in org:
            dic['id'] = j.id
            dic['organization_name'] = j.organization_name
            dic['premiumUser'] = j.premiumUser
          member_organization_data.append(dic)
      
    
      return response.Response({
          'owner_organizations': owner_organization_data,
          'member_organizations': member_organization_data,
          })  

########### Organization MemberAll ########
class OrganizationMember(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def get(self, request, org_id):
    try:
      org = Organization.objects.get(id = org_id)
      
      lst = []
      k = 0
      dic =[]
      # for i in org.member.all():
      #   k = i.id        
      #   lst.append(i.email)
      #   # print(i.rol
      member = addMember.objects.filter(organization = org)
      
      j = 0
      for i in member: 
        ls = {}
        ls['role'] = i.role
        ls['is_company'] = i.is_company
        ls['email'] = i.email
        ls['id'] = i.id
        dic.append(ls)
      print(dic)
      return response.Response(dic,status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
      return response.Response("Orgnization information not valid")
  
########### Organization Member Remove ###### 
class MemberRemoveView(generics.DestroyAPIView):
    queryset = addMember.objects.all()
    serializer_class = addMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')    
        print(pk)
        try:   
            member_id = addMember.objects.get(pk = pk)
            try:
              member = addMember.objects.get(organization__member = self.request.user)
              if member.role == 'Contributor' or member.role == 'Consumer':
                return response.Response({'message':"You don't have permission to remove member."})
              member_id.delete()
              return response.Response({"message":"Member Remove Successfully"})
            except: 
              member_id.delete()
              return response.Response({'message':'Delete Successfully'})
        except addMember.DoesNotExist:
            return response.Response({
                'message':'Not valid asset'
            })

####### Invited Code Member Add #######

        
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
    
    
    org_m = addMember.objects.filter(organization__organization_name = organization_name)
    
    for i in org_m:
      if i.user == request.user:
        if i.role == 'Contributor' or i.role == 'Consumer':
          print(i.role)
          return response.Response({"msg": "You don't have permission add member option."})
    try:
      user = User.objects.get(email=email)
      if request.user == user:
        return response.Response("Not Valid Email")
      try:
        organization = Organization.objects.get(organization_name=organization_name)
        if len(org_m) >= 3 and organization.premiumUser == False:
          return response.Response({"msg":"Your Organization has exceeded the number of members limit and you must purchase Premium to add additional members."}) 
        if organization.owner == user:
          return response.Response({
            "msg":"Not Valid Email"
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
        body = f'''{user.name} has invited You to collaborate on the {organization_name} Organization

You can accept this invitation to click the link ''' + link +  uid + '/'+ token + '/' + org_name
        
      # data = {
      #   'subject':'Confirm your Organization account on assetOptimizeX',
        data = {
          'subject':f'{user.name} invited you to {organization_name}',
          'body':body,
          'to_email':email,
        }
        Util.send_email(data)
        
        return response.Response({'message':"Invited Link send."})
        
      except Organization.DoesNotExist:
        return response.Response({'msg':"Organization not register"})
    except User.DoesNotExist:
      return response.Response({"msg":"user not register"})
               
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
 
########### Organization Invited Member Request View #######
class InvitedCodeaddMemberView(views.APIView):
  permission_classes= [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  def post(self, request):
    serializer = InvitedaddMemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    invited_code = serializer.data.get('invited_code')
    organization_name = serializer.data.get('organization_name')
    
    try: 
      org = Organization.objects.get(organization_name=organization_name)
      try:
        user = User.objects.get(id = request.user.id) 
         
        if org.owner == user:
          return response.Response({'message':'You are Owner This organization.'})
        if len(org.member.all()) >= 3 and org.premiumUser == False:
          return response.Response({'message':'The number of members in this organization has exceeded the limit. You cannot join this organization'})
        
        for i in org.member.all():
          if i.email == user.email:
            return response.Response({'message': "Already You added This Organization Member."})
        role = 'Consumer'
        if org.invited_code == invited_code:  
          member = addMember.objects.create(user=user, organization=org, email=user.email, role=role, is_company=True)
          member.save()
          org.save()
          return response.Response({'message':'You have Viewer permission in this Organization.'})
        else:
          return response.Response({'message':"Information didn't match"})
      except User.DoesNotExist:
        return response.Response({'message':'Authentication credentials were not provided.'})
    except Organization.DoesNotExist:
      return response.Response({'message':"Organization didn't find"})


########## Member Permission Edit ########
class MemberPermissionUpdateView(generics.UpdateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = MemberPermissionUpdateSerializer
  queryset = addMember.objects.all()
     
  def perform_update(self, serializer):
        pk = self.kwargs.get('pk')    
        print(pk)
        try:   
            member_id = addMember.objects.get(pk = pk)
            try:
              member = addMember.objects.get(organization__member = self.request.user)
              if member.role == 'Contributor' or member.role == 'Consumer':
                return response.Response({'message':"You don't have permission to Edit member."})
              serializer.save()
              return response.Response({"message":"Member  Update Successfully"})
            except: 
              serializer.save()
              return response.Response({'message':'Update Successfully'})
        except addMember.DoesNotExist:
            return response.Response({
                'message':'Not valid'
            })
 
 
class MemberPermissionUpdateview(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  def get(self, request, pk):
    member = addMember.objects.get(pk = pk)
    lst = {}
    lst['role'] = member.role
    lst['email'] = member.email
    lst['is_company'] = member.is_company
    return response.Response(lst, status=status.HTTP_200_OK)
  