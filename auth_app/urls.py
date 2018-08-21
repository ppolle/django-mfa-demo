from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('^sign-up$',views.signup, name = 'signup'),
    url('^login$',views.login,name = 'login'),
    url('^profile$',views.profile,name = 'profile'),
    url('^logout$',views.logout,name = 'logout'),
    url('^activation_sent$',views.activation_sent,name = 'activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<email>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]