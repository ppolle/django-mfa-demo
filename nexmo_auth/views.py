import nexmo
from django.shortcuts import render,redirect
from django.conf import settings


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
		form = PhoneNumberForm(request.POST)
		return render(request,'nexmo/verification.html')

	return redirect('welcome')

