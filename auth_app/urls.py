from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('^sign-up$',views.signup, name = 'signup'),
    url('^login$',views.login,name = 'login'),
]