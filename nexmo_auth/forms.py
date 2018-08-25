from django import forms
from auth_app.models import Profile


class PhoneNumberForm(forms.ModelForm):
	'''
	Form class to create form to accept users phone number
	'''
	class Meta:
		model = Profile
		fields = ('phone_number',)

	def __init__(self,*args, **kwargs):
		super(PhoneNumberForm, self).__init__(*args, **kwargs)
		self.fields['phone_number'].widget.attrs['class'] ='form-control'
		
	#phone_number = forms.IntegerField(label = 'Phone Number',required = True,widget=forms.TextInput(attrs={'class':'form-control'}))
	
class VerifyTokenForm(forms.Form):
	'''
	Form class to create form to accept users phone number
	'''
	token = forms.IntegerField(label = 'Token',required = True,widget=forms.TextInput(attrs={'class':'form-control'}))
	

