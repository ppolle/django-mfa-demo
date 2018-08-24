import nexmo
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages


from .forms import PhoneNumberForm


client = nexmo.Client(key=settings.NEXMO_KEY, secret=settings.NEXMO_SECRET)

# Create your views here.
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
				return redirect('verify')
			else:
				messages.error(request, 'That was a bad request. Please try using a correct phone number')
				return redirect(request.META.get('HTTP_REFERER'))

	else:
		form = PhoneNumberForm()
		return render(request,'nexmo/verification.html',{'form':form})

	

