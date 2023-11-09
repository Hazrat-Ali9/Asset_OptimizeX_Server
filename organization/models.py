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
  organization_logo = models.ImageField(upload_to = 'images/company-logo/', null=True, blank=True,default='org_logo/org-logo.png'  )
  tc = models.BooleanField()
  is_company = models.BooleanField(default=False)
  country = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=50)
  company_phone_number = models.IntegerField(unique=True)
  invited_code = models.IntegerField(null=True, blank=True)
  # member = models.ManyToManyField(addUser)
  premiumUser = models.BooleanField(default=False, null=True, blank=True)
  
  

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

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length= 100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
  
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  order_number = models.CharField(max_length=30)
  ip = models.CharField(max_length=100, blank=True, null = True)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add = True)
  
  
class premiumOrder(models.Model):
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  ordered = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  
class PaymentGateWaySettings(models.Model):
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)
  
  
