from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms  import UserSignupForm,UserAuthForm

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
			login(request,user)

			return redirect('home')
	else:
		form = UserAuthForm()
		return render(request,'authentication/login.html',{'form':form})