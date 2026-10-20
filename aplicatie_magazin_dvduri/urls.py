from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('info/', views.info, name="info"),
    path('exemplu_template', views.exemplu_template, name="exemplu_template"),
    path('exemplu_template2', views.exemplu_template2, name="exemplu_template2"),
    path('log', views.log, name = "log"),
    path('istoric', views.istoric, name = "istoric"),
    path('despre', views.despre, name = "despre"),
    re_path(r'^accesare(?P<id>\d+)$', views.accesare, name = "accesare"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)