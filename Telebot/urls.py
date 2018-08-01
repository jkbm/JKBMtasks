from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "Telebot"
urlpatterns = [
    url(r'^$', views.index, name='home'),
    path('webhook/', views.webhook, name='webhook'),



]