from django.shortcuts import render
from rest_framework import views, response
from contact.models import ContactModel
from contact.serializers import *

# Create your views here.
######## Contact View ###########
class ContactView(views.APIView):
  
  def post(self, request):
    serializer = ContactSerializers(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    serializer.save()
    print(serializer)
    # ContactModel.objects.create(ser)
    return response.Response({'message':'Thank you for providing your contact information. We will be in touch soon.'})

