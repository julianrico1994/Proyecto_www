from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from .models import *
from apps.sucursales.models import Sucursales
from apps.usuarios.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    authenticate, get_user_model
)
from django.utils.translation import ugettext, ugettext_lazy as _



class MyPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={'autofocus': '',
            'class':'form-control'}),
    )

    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'})
                                    #help_text=password_validation.password_validators_help_text_html()
                                    )
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    

class LoginForm(forms.Form):


    username = forms.CharField(max_length = 50,
            widget=forms.TextInput(attrs ={
                    'id':'usernameInput',
                    'placeholder': 'User Name',
                    'class':'form-control'
                }))
    password = forms.CharField(max_length = 50,
            widget = forms.TextInput(attrs = {
                    'type' : 'password',
                    'id':'passwordInput',
                    'placeholder': 'Password',
                    'class':'form-control'
                }))




class EditProfileForm(forms.Form):
    phone_number = forms.CharField(max_length=50,widget = forms.TextInput(attrs={
                                                        'id':'IdInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    address = forms.CharField(max_length=50,widget = forms.TextInput(attrs={
                                                        'id':'IdInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    email = forms.EmailField(max_length=50,widget = forms.TextInput(attrs={
                                                        'id':'IdInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))

    def set_fields(self, username):
        self.user = User.objects.get(username=username)
        self.fields['phone_number'].initial = self.user.phone_number
        self.fields['address'].initial = self.user.address
        self.fields['email'].initial = self.user.email

    def update(self):
        # print "SALVADO!"
        #user = super(EditProfileForm, self).save(commit=False)
        self.user.phone_number = self.cleaned_data['phone_number']
        self.user.address = self.cleaned_data['address']
        self.user.email = self.cleaned_data['email']
        self.user.save()


    class Meta:
        model = User


class MyUserCreationForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    username=forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'IdInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))

    sex = forms.ChoiceField(choices=[("M", "M"),
        ("F", "F"),], widget=forms.RadioSelect(attrs={
            'class':'flat-red'
            }))

    YEARS = [y for y in range(1930,2015)]
    birth_date = forms.DateField(widget=SelectDateWidget(years=YEARS,
                                                        attrs={'class':'form-control select2 select2-hidden-accessible',
                                                        'type':'date'}))
    charge = forms.ChoiceField(choices=[("Gerente","Gerente"),
                                ("Vendedor", "Vendedor"), ("Jefe Taller", "Jefe Taller")],
                                    widget= forms.RadioSelect(attrs={
                                                        'id':'chargeInput',
                                                        'type':'radio',
                                                        'class':'flat-red'
                                   }))
    phone_number = forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'telephoneInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    id_document = forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'IdInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    email = forms.EmailField(max_length = 255,
                              widget = forms.TextInput(attrs={
                                                       'id':'emailInput',
                                                       'class':'form-control'
                                }))
    address = forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'addressInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    first_name = forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'firstNameInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    last_name = forms.CharField(max_length = 50, 
                                  widget = forms.TextInput(attrs={
                                                        'id':'lastNameInput',
                                                        'type':'text',
                                                        'class':'form-control'
                                   }))
    password1=forms.CharField(max_length = 50, 
                                  widget = forms.PasswordInput(attrs={
                                                        
                                                        'class':'form-control'
                                   }))
    password2=forms.CharField(max_length = 50, 
                                  widget = forms.PasswordInput(attrs={
                                                        
                                                        'class':'form-control'
                                   }))
    branch = forms.ModelChoiceField(queryset=Sucursales.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class':'form-control select2 select2-hidden-accessible'}))


    def save(self, commit=True):
        if self.cleaned_data['charge'] == "Gerente":
            self.cleaned_data['branch'] = ''
        return super(MyUserCreationForm, self).save(commit)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name","last_name","username", "email","address", "phone_number", 
            "id_document","sex", "charge", "birth_date", "branch")

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['branch'].required = False

