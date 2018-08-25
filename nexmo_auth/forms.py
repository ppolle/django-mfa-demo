from django import forms


class PhoneNumberForm(forms.Form):
	'''
	Form class to create form to accept users phone number
	'''
	phone_number = forms.IntegerField(label = 'Phone Number',required = True,widget=forms.TextInput(attrs={'class':'form-control'}))
	
class VerifyTokenForm(forms.Form):
	'''
	Form class to create form to accept users phone number
	'''
	token = forms.IntegerField(label = 'Token',required = True,widget=forms.TextInput(attrs={'class':'form-control'}))
	