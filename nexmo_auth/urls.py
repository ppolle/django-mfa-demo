from django.conf.urls import url
from . import views

app_name = 'nexmo_auth'


urlpatterns=[
	url('^signupVerification$',views.signupVerification,name = 'signupVerification'),
	url('^verify',views.verify,name = 'verify'),
  
]