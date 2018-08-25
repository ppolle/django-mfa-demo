import nexmo
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages


from .forms import PhoneNumberForm,VerifyTokenForm


client = nexmo.Client(key=settings.NEXMO_KEY, secret=settings.NEXMO_SECRET)

# Create your views here.
@login_required(login_url='/login/')
def signupVerification(request):
	'''
	This function wil send codes to the users phone
	'''
	if request.method == 'POST':
		form = PhoneNumberForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data.get('phone_number')
			response = client.start_verification(number=phone_number, brand='Peter Polle')
			if response['status'] == '0':
				request.session['verification_id'] = response['request_id']
				request.session['phone_number'] = phone_number
				return redirect('nexmo_auth:verify')
			else:
				messages.error(request, 'That was a bad request. Please try using a correct phone number')
				return redirect(request.META.get('HTTP_REFERER'))
		else:
			messages.error(request, 'Wrong phone number format')
			return redirect(request.META.get('HTTP_REFERER'))
	else:
		form = PhoneNumberForm()
		return render(request,'nexmo/verification.html',{'form':form})

@login_required(login_url='/login/')
def verify(request):
	'''
	This function will verify a phone number
	'''
	if request.method == 'POST':
		form = VerifyTokenForm(request.POST)
		if form.is_valid():
			token = form.cleaned_data.get('token')
			response = client.check_verification(request.session['verification_id'], code=token)

			if response['status'] == '0':
				request.user.profile.phone_number = request.session['phone_number']
				messages.success(request,'Succesfull verification')
				return redirect('profile')
			else:
				messages.error('Wrong token. Please try again')
				return redirect(request.META.get('HTTP_REFERER'))

	else:
		form = VerifyTokenForm()
		return render(request,'VerifyToken.html',{'form':form})

@login_required(login_url='/login/')
def signinVerification(request):
	'''
	This view function will manage signin with a nexmo 2fa
	'''
	phone_number = request.user.profile.phone_number
	response = client.start_verification(number=phone_number, brand='Peter Polle')
	if response['status'] == '0':
		request.session['verification_id'] = response['request_id']
		request.session['phone_number'] = phone_number
		return redirect('nexmo_auth:verify')
@login_required(login_url='/login/')
def nexmoAuth(request):
	'''
	This view function will manage nexmo signin views
	'''
	if request.user.profile.phone_number:
		return redirect('nexmo_auth:signinVerification')
	else:
		return redirect('nexmo_auth:signupVerification')
    		


	

