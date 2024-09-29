from django import forms

class MaterialForm(forms.Form):
    material = forms.CharField(max_length=100, label='Material')
    cantidad = forms.IntegerField(label='Cantidad')
