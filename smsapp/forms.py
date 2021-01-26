from django import forms


class CreateSms(forms.Form):
    phone_number = forms.CharField(
                        label='phone number',
                        max_length=100,
                        min_length=3,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'start with country code e.g +254xxx '}))  # noqa: E501
    message = forms.CharField(
                        label='message',
                        max_length=255,
                        min_length=3,
                        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 20}))  # noqa: E501
