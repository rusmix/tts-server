# api/urls.py

from django.urls import path
from .views import GetAudioView, SendParamsView, GetHistoryView, GetFileView
from django.views.generic import TemplateView

urlpatterns = [
    path('get-audio/', GetAudioView.as_view(), name='get-audio'),
    path('send-params/', SendParamsView.as_view(), name='send-params'),
    path('get-history/', GetHistoryView.as_view(), name='get-history'),
    path('get-file/', GetFileView.as_view(), name='get-file'),
    path('/', TemplateView.as_view(template_name="main.html")),
]
