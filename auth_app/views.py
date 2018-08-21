from django.contrib.auth import login as user_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms  import UserSignupForm,UserAuthForm,EmailConfirmationForm

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
		form = EmailConfirmationForm()
		return render(request,'email.html',{'form':form})