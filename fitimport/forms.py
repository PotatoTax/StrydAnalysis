from django.forms import forms


class FITUploadForm(forms.Form):
    file = forms.FileField(label="FIT file to upload")
