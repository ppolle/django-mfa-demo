from django.contrib.auth import login as user_login, authenticate, logout as user_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms  import UserSignupForm,UserAuthForm,EmailConfirmationForm,TwoFactorChoicesForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django_mfa.models import *

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# Create your views here.
def welcome(request):
	'''
	View function to render the landing page
	'''
	if request.user.is_authenticated:
		return redirect('profile')
	else:
		return render(request,'index.html')

def signup(request):
	'''
	View function to handle signup functionality
	'''
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			form.save()
			
			return redirect('login')

	else:
		form = UserSignupForm()
		return render(request,'authentication/signup.html',{'form':form})

def login(request):
	'''
	View function to handle login functionality
	'''
	if request.method == 'POST':
		form = UserAuthForm(request.POST)
		if form.is_valid():
			username =  form.cleaned_data.get('username')
			password  =  form.cleaned_data.get('password')
			user = authenticate(username = username,password=password)
			if user is not None:

				user_login(request,user)
				messages.success(request, f'Welcome back {username}!')
				return redirect('profile')

			else:
				messages.error(request, 'Wrong username/paswword combination.Please try again!')
				return redirect(request.META.get('HTTP_REFERER'))
	else:
		form = UserAuthForm()
		return render(request,'authentication/login.html',{'form':form})

@login_required(login_url='/login/')
def profile(request):
	'''
	View function to handle sending email links
	'''
	if request.user.email:
		if is_mfa_enabled(request.user):
			return redirect('mfa:verify_otp')
		elif request.user.profile.phone_number:
			return redirect('nexmo_auth:signinVerification')
		else:
			return redirect('authChoice')
		
	else:
		if request.method == 'POST':
			form = EmailConfirmationForm(request.POST)
			if form.is_valid():
				current_site = get_current_site(request)
				mail_subject = 'Activate your Email Address'
				message = render_to_string('email/activate_email.html',{
					'user': request.user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
					'email': urlsafe_base64_encode(force_bytes(form.cleaned_data.get('email'))),
					'token':account_activation_token.make_token(request.user),
					})
				reciever_email = form.cleaned_data.get('email')
				email = EmailMessage(mail_subject,message,to=[reciever_email])
				email.send()
			
				return redirect('activation_sent')
		else:
			
			form = EmailConfirmationForm()
			return render(request,'email.html',{'form':form})

@login_required(login_url='/login/')
def logout(request):
	'''
	View function handle logout functionality
	'''
	user_logout(request)
	return redirect('welcome')

@login_required(login_url='/login/')
def activation_sent(request):
	'''
	View function to render page after activation email has been sent
	'''
	return render(request,'email/activation_sent.html')

@login_required(login_url='/login/')
def activate(request, uidb64,email,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        email = force_text(urlsafe_base64_decode(email))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
    	Profile.objects.filter(user = request.user).update(email_confirmed = True)
    	User.objects.filter(id = user.id).update(email = email)
    	messages.success(request, f'Hey {user.username}! You have succesfully activated your email address!')
    	return redirect('profile')
    else:
        return render(request,'email/invalid.html')

def auth(request):
	'''
	This view function will render a page that shows a 2fa form selection
	'''

	two_factor = request.GET.get('two_factor')
	if two_factor == "google_auth":
		return redirect('mfa:configure_mfa')
	if two_factor == "nexmo_auth":
		return redirect('nexmo_auth:signupVerification')
	
		
		
		
def authChoice(request):
	'''
	This view function will render the auth choice form
	'''
	return render(request,'authentication/auth.html')