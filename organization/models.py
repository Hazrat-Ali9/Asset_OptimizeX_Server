from django.db import models
from account.models import User
from django.utils.text import slugify
# Create your models here.
class Organization(models.Model):
  user = models.ForeignKey(User, on_delete= models.CASCADE)
  organization_name = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=200)
  description = models.TextField(max_length=1000)
  created_date = models.DateTimeField(auto_now_add=True)
  organization_logo = models.ImageField(upload_to = 'images/company-logo/')
  tc = models.BooleanField()
  is_company = models.BooleanField(default=False)
  country = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=50)
  company_phone_number = models.IntegerField(unique=True)
  

  def __str__(self):
      return self.organization_name
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.organization_name)
    super(Organization, self).save(*args, **kwargs)
    

  
  
  
