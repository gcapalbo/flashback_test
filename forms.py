from django import forms

class SendMessageForm(forms.Form):
    mobile_number = forms.CharField(max_length=20)
    message = forms.CharField(max_length=140,initial="Please call back to this number.")

