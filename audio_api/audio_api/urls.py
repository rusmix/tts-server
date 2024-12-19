# audio_api/urls.py

import os  # Import the os module
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name="main.html")),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static('/media/', document_root=os.path.join(settings.BASE_DIR, 'media'))
