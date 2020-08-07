from django import forms


class ActivityDataForm(forms.Form):
    power = forms.BooleanField(label="Power", initial=True, required=False)
    speed = forms.BooleanField(label="Speed", required=False)
    heart_rate = forms.BooleanField(label="Heart Rate", required=False)
    cadence = forms.BooleanField(label="Cadence", required=False)
    ground_time = forms.BooleanField(label="Ground Time", required=False)
    air_power = forms.BooleanField(label="Air Power", required=False)
    form_power = forms.BooleanField(label="Form Power", required=False)
