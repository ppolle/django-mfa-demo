from django.contrib.auth import login as user_login, authenticate, logout as user_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms  import UserSignupForm,UserAuthForm,EmailConfirmationForm
from django.contrib.auth.models import User

# Create your views here.
def welcome(request):
	'''
	View function to render the landing page
	'''
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
				return redirect('profile')

			else:
				return redirect(request.META.get('HTTP_REFERER'))
	else:
		form = UserAuthForm()
		return render(request,'authentication/login.html',{'form':form})

def profile(request):
	'''
	View function to handle sending email links
	'''
	if request.user.email:
		return render(request,'homepage.html')
	else:
		if request.method == 'POST':
			form = EmailConfirmationForm(request.POST)
			if form.is_valid():
				email = form.cleaned_data.get('email')
				User.objects.filter(id = request.user.id).update(email = email)
				return redirect('profile')
		else:
			form = EmailConfirmationForm()
			return render(request,'email.html',{'form':form})

def logout(request):
	'''
	View function handle logout functionality
	'''
	user_logout(request)
	return redirect('welcome')