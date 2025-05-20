from django.contrib import admin
from django.urls import path ,include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# def home_view(request):
#     return HttpResponse("🎉 Hello from AWS Django App!")

urlpatterns = [
    # path('', home_view),  # root view
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# from django.contrib import admin
# from django.urls import path ,include
# from django.http import HttpResponse
# from django.conf import settings
# from django.conf.urls.static import static



# urlpatterns = [
   
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')), 
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)