from django import forms
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'Repeat Password',
        widget = forms.PasswordInput
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match")
        return cd['password2']
        
        
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        if User.objects.filter(email = data).exists():
            raise forms.ValidationError("email already in use")
        return data