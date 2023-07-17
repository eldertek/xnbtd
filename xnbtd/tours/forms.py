from django import forms


class DeliveryForm(forms.Form):
    date = forms.DateField()
    points_loaded = forms.IntegerField()
    points_delivered = forms.IntegerField()
    packages_loaded = forms.IntegerField()
    packages_delivered = forms.IntegerField()
    avp_relay = forms.CharField()
    shd = forms.CharField()
    eo = forms.CharField()
    pickup_point = forms.CharField()
