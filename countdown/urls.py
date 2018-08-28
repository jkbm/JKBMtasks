from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "countdown"
urlpatterns = [
    url(r'^$', views.index, name='home'),
    path("countdown/", views.countdown, name='countdown'),
    path("countdown/<cd_id>", views.send_countdown, name='countdown_send'),

]