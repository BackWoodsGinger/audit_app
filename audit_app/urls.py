
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from audits import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('audits/', include('audits.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
