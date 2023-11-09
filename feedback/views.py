from django.shortcuts import render
from rest_framework import views, response, permissions, status
from feedback.models import Feedbackmodel
from feedback.serializers import *
from account.renders import UserRenderer
from organization.models import Organization

########## User FeedBack View ########
class FeedbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
      user = request.user
      message = request.data.get('message')
      organization = request.data.get('organization_name')
      org_position = request.data.get('org_position')
      
      try:  
        org = Organization.objects.get(organization_name=organization) 
        feed = Feedbackmodel.objects.filter(organization=org)
        # for i in feed:
        #   if i.user == request.user:
        #     return response.Response({'message':'You have already given feedback.'})
        flag = False
        if org.owner == request.user:
          flag = True
          
        if flag == False:
          for i in org.member.all():
            if i.email == request.user.email:
              flag = True
        if flag == True:
          feedback = Feedbackmodel(user=user, organization=org, message=message, org_position=org_position, feedback_approve=False)
          feedback.save()
          return response.Response({'message':'Thank you for your feedback, we will review and approve your feedback.'})
        else:
          return response.Response({'message':'You are not allowed to provide feedback to this Organization.'})
      except Organization.DoesNotExist:
        return response.Response({'message':'No Organization found with this name.'})    

######## Show Feedback View #######
class ShowFeedBackView(views.APIView):
  permission_classes = [permissions.AllowAny]
  
  def get(self, request):
    feed = Feedbackmodel.objects.filter(feedback_approve = True)
    
    lst = []
    for i in feed:
      dic = {}
      dic['user'] = i.user.name
      dic['message'] = i.message
      dic['org_position'] = i.org_position
      dic['organization_name'] = i.organization.organization_name
      dic['image'] = i.user.image.url
      lst.append(dic)
    return response.Response(lst, status=status.HTTP_200_OK)
    
    

