from django.db import models
from account.models import User
from organization.models import Organization
# Create your models here.

class Feedbackmodel(models.Model):
  RATING = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
  message = models.TextField(max_length=500)
  org_position = models.CharField(max_length=200, null=True)
  feedback_approve = models.BooleanField(default=False, null=True)
  
 
  