from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/user/', include('account.urls')),
     path('api/organization/', include('organization.urls')),

     path('api/', include('uploadAsset.urls')),
     path('api/category/', include('category.urls')),
     path('api/library/', include('library.urls')),
     
     path('api/share/', include('share_assets.urls')),
     
     path('api/', include('contact.urls')),
     path('api/', include('feedback.urls')),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
