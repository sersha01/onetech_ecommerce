from django import forms
from .models import Address, User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ('name', 'username', 'phone', 'password1', 'password2')

        labels = {
            'name':'Full Name',
            'username':'E-mail',
            'phone':'Phone',
            'password1':'Password',
            'password2':'Confirm Password',
        }

    def __init__(self, *args ,**kwargs):
        super(UserForm, self).__init__(*args ,**kwargs)
        self.fields['name'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Enter your Name', 'id':'name', 'name':'name'})

        self.fields['username'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Enter your E-mail', 'id':'email', 'name':'email', 'type':'email'})

        self.fields['phone'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Phone Number', 'id':'phone', 'name':'phone', 'minlength':'9', 'maxlength':'10', 'type':'number', 'min':'None', 'max':'None'})

        self.fields['password1'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Enter Password', 'id':'password', 'name':'password', 'minlength':'6'})

        self.fields['password2'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Confirm your Password', 'id':'confirm_password', 'name':'confirm_password'})

class AddressForm(forms.ModelForm):
    class Meta:

        model = Address
        fields = ('name', 'address', 'city', 'state', 'pincode', 'number', 'user')
        exclude = ['user']
        widgets = {
          'address': forms.Textarea(attrs={'rows':4})
        }
        labels = {
            'name' : 'NAME',
            'address' : 'ADDRESS',
            'city' : 'CITY',
            'state' : 'STATE',
            'pincode' : 'PIN CODE',
            'number' : 'PHONE'
                    }

    def __init__(self, *args ,**kwargs):
        super(AddressForm, self).__init__(*args ,**kwargs)
        self.fields['name'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Enter your Name', 'id':'name', 'name':'name'})
        
        self.fields['address'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Address', 'id':'address', 'name':'address'})
        
        self.fields['city'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'City', 'id':'city', 'name':'city'})
        
        self.fields['state'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'State', 'id':'state', 'name':'state'})
        
        self.fields['pincode'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Pin Code', 'id':'pincode', 'name':'pincode'})
        
        self.fields['number'].widget.attrs.update(
            {'class':'form-control form-control-lg py-1 rounded', 'placeholder':'Phone Number', 'id':'number', 'name':'number'})