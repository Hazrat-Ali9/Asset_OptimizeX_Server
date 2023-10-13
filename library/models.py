from django.db import models
from organization.models import Organization
from django.utils.text import slugify
# Create your models here.

class Library(models.Model):
    organization = models.ForeignKey(Organization, on_delete= models.CASCADE)
    library_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.library_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.library_name)
        super(Library, self).save(*args, **kwargs)
        
