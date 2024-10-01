from django import forms
from django.db import models
from django.conf import settings


class Material(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Cambia auth.User por settings.AUTH_USER_MODEL
    material = models.CharField(max_length=255)  # Campo para el nombre del material
    cantidad = models.PositiveIntegerField()  # Campo para la cantidad

    def __str__(self):
        return self.material
    
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['material', 'cantidad']  # Asegúrate de que estos campos existan en tu modelo