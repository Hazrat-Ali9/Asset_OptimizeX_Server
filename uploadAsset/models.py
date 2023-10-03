from django.db import models
from organization.models import Organization
from category.models import Category
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class uploadAsset(models.Model):
  user = models.ForeignKey(Organization, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  file_type = models.FileField(upload_to='images/company/asset/')
  upload_date = models.DateTimeField(auto_now_add= True)
  tags = models.ManyToManyField(Tag, blank=True)
  location = models.CharField(max_length=200)
  comment = models.CharField(max_length=300)
  expiry_date = models.DateTimeField(auto_now_add=True) # Research how to fixed date delete asset
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  
  def __str__(self):
      return self.title
  
  
  

