from django import forms

class PredictionForm(forms.Form):

    quantity = forms.IntegerField()

    price = forms.FloatField()



from django import forms

class PredictionForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity', min_value=1)
    price = forms.FloatField(label='Price', min_value=0)