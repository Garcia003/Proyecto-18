"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404

from core import views

handler404 = views.page_not_found404

URLS_TOTAL = [
    path('admin/', admin.site.urls),
    path('qrcode/<qrid>/', views.qrLink,name='qrLink'),
    path('importExcel/', views.importExcel,name='importExcel'),
    path('form/<qrid>/', views.registrar_afiliacion,name='formulario'),
    path('stats/', views.stats_general, name='stats_general'),
    path('export/', views.exportPointQr, name='exportPointQr'),
    path('stats/<str:qridd>', views.stats_general, name='stats'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('uqr/', include(URLS_TOTAL))
]
