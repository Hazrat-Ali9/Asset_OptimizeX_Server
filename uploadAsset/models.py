from django.db import models
from library.models import Library
from account.models import User
from django.utils import timezone

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


# class uploadAsset(models.Model):
#   user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
#   library = models.ForeignKey(Library, on_delete=models.CASCADE)
#   title = models.CharField(max_length=100)
#   description = models.TextField(max_length=500,blank=True)
#   asset = models.FileField(upload_to='images/company/asset/',default=None)
#   tags = models.ManyToManyField(Tag, blank=True)
#   location = models.CharField(max_length=200)
#   comment = models.CharField(max_length=300,blank=True)
#   crerated_at = models.DateTimeField(auto_now_add=True) 
#   updated_at = models.DateTimeField(auto_now=True) 
  
#   def __str__(self):
#       return self.title
  
  
  

class AssetVersion(models.Model):
    title = models.CharField(max_length=100)
    asset = models.FileField(upload_to='images/company/asset_versions/')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class uploadAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    asset = models.FileField(upload_to='images/company/asset/')
    tags = models.ManyToManyField(Tag, blank=True)
    location = models.CharField(max_length=200)
    comment = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    versions = models.ManyToManyField(AssetVersion, blank=True)

    def save(self, *args, **kwargs):
        # Check if the asset file has changed
        if self.pk:
            existing_asset = uploadAsset.objects.get(pk=self.pk)
            if existing_asset.asset != self.asset:
                # Create a new version if the asset has changed
                asset_version = AssetVersion(asset=existing_asset.asset)
                asset_version.save()
                self.versions.add(asset_version)
        super(uploadAsset, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
