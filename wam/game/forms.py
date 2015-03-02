from django import forms

class UploadFileForm(forms.Form):
    ai_title = forms.CharField(max_length=50)
    ai_code = forms.FileField()

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UserLoginForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
