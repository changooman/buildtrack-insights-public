from django.contrib import admin
from django.urls import path
from buildtrack import views as buildtrack_views
from django.views.generic import TemplateView

urlpatterns = [
    # Homepage URL
    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),

    # URL for the BuildTrack app
    path('buildtrack/', buildtrack_views.index, name='buildtrack'),

    # Admin site URLs
    path('admin/', admin.site.urls),
]
