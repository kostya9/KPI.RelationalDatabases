from django.conf.urls import url
import core.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pilots/', views.pilots, name="pilots")
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)