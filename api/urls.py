from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^matrix$', views.matrix),
    url(r'^currencies$', views.currencies)
]
