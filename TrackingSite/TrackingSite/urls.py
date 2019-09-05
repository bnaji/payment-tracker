"""TrackingSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.views.generic import TemplateView
from .views import home, send_push
from django.conf import settings
from django.conf.urls.static import static
from payments.tasks import lessons_for_week
from background_task.models import Task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('payments/', include('payments.urls')),
    url(r'^webpush/', include('webpush.urls')),
    path('', home),
    path('send_push', send_push),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))            
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

lessons_for_week(repeat=Task.WEEKLY)

