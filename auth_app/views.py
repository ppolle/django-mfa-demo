from django.shortcuts import render

# Create your views here.
def welcome(request):
	'''
	View function to render the landing page
	'''
	return render(request,'index.html')