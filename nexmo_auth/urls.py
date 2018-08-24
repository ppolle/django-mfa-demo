from django.conf.urls import url
from . import views

app_name = 'nexmo_auth'


urlpatterns=[
	url('^signupVerification$',views.verification,name = 'signupVerification'),
  
]