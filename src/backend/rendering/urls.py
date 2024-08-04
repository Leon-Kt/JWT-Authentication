from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from rendering.views import index, render_login


urlpatterns = [
    path('', index, name='index'),
    path('login', render_login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
