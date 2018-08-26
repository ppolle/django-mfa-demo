from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

TWO_FACTOR_CHOICES = (
('google_auth','Use An App'),
('nexmo_auth','Use An SMS Service'),
)

class UserSignupForm(UserCreationForm):
	'''
	Form class to create a signup form
	'''
	class Meta:
		model = User
		fields = ('username','password1','password2')

	def __init__(self,*args, **kwargs):
		super(UserSignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] ='form-control'
		self.fields['password1'].widget.attrs['class'] ='form-control'
		self.fields['password2'].widget.attrs['class'] ='form-control'
		


class UserAuthForm(forms.Form):
	'''
	Form class to create login form
	'''
	username = forms.CharField(label = 'Username',max_length = 30,required = True,widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label = 'Password',required = True,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class EmailConfirmationForm(forms.Form):
	'''
	Form class to render email input form
	'''

	email = forms.EmailField(max_length=254,label = 'Email', required= True, help_text='Required. Inform a valid email address.',widget=forms.TextInput(attrs={'class':'form-control'}))

class TwoFactorChoicesForm(forms.Form):
	'''
	This form class will render a form to select a choice for 2fa
	'''
	two_factor = forms.ChoiceField(
		widget=forms.CheckboxSelectMultiple,
        choices=TWO_FACTOR_CHOICES,
		)