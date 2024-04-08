from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from main import settings


urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('', include('accounts.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
