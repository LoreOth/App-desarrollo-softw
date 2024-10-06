from django import forms
from django.db import models
from django.conf import settings


class Material(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Referencia al usuario
    material = models.CharField(max_length=255)  # Nombre del material
    cantidad = models.PositiveIntegerField()  # Cantidad registrada
    supervisado = models.BooleanField(default=False)  # Indica si el material ha sido supervisado

    def __str__(self):
        return self.material
class Materiales(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del material
    cantidad_total = models.PositiveIntegerField()  # Cantidad total disponible

    def __str__(self):
        return self.nombre

    
class MaterialForm(forms.ModelForm):
    material = forms.ModelChoiceField(
        queryset=Materiales.objects.all(),  # Consulta para recuperar los materiales disponibles
        empty_label="Seleccione un material",
        widget=forms.Select(attrs={'class': 'form-control'})  # Personaliza el widget si es necesario
    )

    class Meta:
        model = Material
        fields = ['material', 'cantidad']
