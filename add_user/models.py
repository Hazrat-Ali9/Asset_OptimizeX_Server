from django.db import models
from organization.models import Organization
from add_user.content import *
# Create your models here.



class addUser(models.Model):
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
  email = models.EmailField(max_length=200, unique=True)
  permission = models.CharField(max_length=50, choices=PERMISSION)
  is_addUser = models.BooleanField(default=False)
  is_company = models.BooleanField(default=False)
  
  def __str__(self):
      return self.email


  


