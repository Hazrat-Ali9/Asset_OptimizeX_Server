from django.contrib import admin
from .models import Library

# Register your models here.

class LibraryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('library_name',)}
  list_display = ['id','library_name', 'created_date']
admin.site.register(Library, LibraryAdmin)