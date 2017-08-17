from django.conf.urls import url

from . import views

app_name = 'lights'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'ajax/button_pressed/$', views.button_pressed, name='button_pressed'),
    url(r'ajax/rgb_message/$', views.rgb_message, name='rgb_message'),
    url(r'ajax/verify_password/$', views.verify_password, name='verify_password'),
    url(r'ajax/modify_life/$', views.modify_life, name='modify_life'),
    url(r'ajax/verify_token/$', views.verify_token, name='verify_token')
]
