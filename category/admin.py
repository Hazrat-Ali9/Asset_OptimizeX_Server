from django.contrib import admin
from category.models import Category
# Register your models here.
class assetCategory(admin.ModelAdmin):
  prepopulated_fields = {'slug':('category_name',)}
  list_display = ['category_name', 'created_at']
  
admin.site.register(Category, assetCategory)  
