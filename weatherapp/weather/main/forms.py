from django import forms

class CityWeather(forms.Form):
    city = forms.CharField(max_length=120)