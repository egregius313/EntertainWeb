from django.conf.urls import url

from . import views

app_name = 'lights'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'ajax/button_pressed/$', views.button_pressed, name='button_pressed')
    ]
