from django.conf.urls import url
from . import views

app_name = 'nexmo_auth'


urlpatterns=[
	url('^signupVerification$',views.signupVerification,name = 'signupVerification'),
	url('^signinVerification$',views.signinVerification,name = 'signinVerification'),
	url('^verify',views.verify,name = 'verify'),
	url('^nexmoAuth$',views.nexmoAuth,name = 'nexmoAuth'),
  
]