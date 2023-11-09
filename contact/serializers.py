from rest_framework import serializers
from contact.models import *

class ContactSerializers(serializers.ModelSerializer):
  class Meta:
    model = ContactModel
    fields = ['name', 'email', 'message']
  