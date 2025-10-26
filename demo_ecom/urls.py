from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


from core.views import index, about

urlpatterns = [
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='core/robots.txt', )),
    path('', include('userprofile.urls')),
    path('', include('store.urls')),
    path('', index, name='index'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
