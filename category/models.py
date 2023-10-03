from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
  category_name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  description = models.TextField(max_length=255, blank=True)
  cat_image = models.ImageField(upload_to = 'images/company/categories', blank = True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.category_name)
    super(Category, self).save(*args, **kwargs)
  
  def __str__(self):
      return self.category_name
  