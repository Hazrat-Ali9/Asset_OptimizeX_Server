from django.contrib import admin
from uploadAsset.models import uploadAsset,AssetVersion,Tag
# Register your models here.

class AssetVersionAdmin(admin.ModelAdmin):
    list_display = ('asset_name','created_at')

    def asset_name(self, obj):
        return obj.asset.name if obj.asset else ''
    asset_name.short_description = 'Asset Name'

class uploadAssetAdmin(admin.ModelAdmin):
  list_display = ['title']
    
admin.site.register(uploadAsset, uploadAssetAdmin)
admin.site.register(AssetVersion, AssetVersionAdmin)
admin.site.register(Tag)