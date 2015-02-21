from django import forms

class UploadFileForm(forms.Form):
    player1_ai_title = forms.CharField(max_length=50)
    player1_ai_code = forms.FileField()
    player2_ai_title = forms.CharField(max_length=50)
    player2_ai_code = forms.FileField()
