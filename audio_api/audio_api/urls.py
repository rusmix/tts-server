# audio_api/urls.py

import os  # Import the os module
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static('/media/', document_root=os.path.join(settings.BASE_DIR, 'media'))
