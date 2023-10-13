from django.db import models
from account.models import User
from django.utils.text import slugify

# Create your models here.
class Organization(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='owned_organizations', null=True, blank=True)
  member = models.ManyToManyField(User, through='addMember')
  
  organization_name = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=200, null=True, blank=True)
  description = models.TextField(max_length=1000)
  created_date = models.DateTimeField(auto_now_add=True)
  organization_logo = models.ImageField(upload_to = 'images/company-logo/', null=True, blank=True)
  tc = models.BooleanField()
  is_company = models.BooleanField(default=False)
  country = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=50)
  company_phone_number = models.IntegerField(unique=True)
  # member = models.ManyToManyField(addUser)
  

  def __str__(self):
      return self.organization_name
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.organization_name)
    super(Organization, self).save(*args, **kwargs)
    
class addMember(models.Model):
  PERMISSION = (
  ('Admin', 'Admin'),
  ('Contributor', 'Contributor'),
  ('Consumer', 'Consumer'),
)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
  email = models.CharField(max_length=200)
  role = models.CharField(max_length=100, choices=PERMISSION)
  is_company = models.BooleanField(default=False)
  

  
  
  
  
