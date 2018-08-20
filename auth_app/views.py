from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username =  form.cleaned_data.get('username')
			password  =  form.cleaned_data.get('password1')
			user = authenticate(username = username,password=password)
			return redirect('login')

	else:
		form = UserCreationForm()
		return render(request,'authentication/signup.html',{'form':form})