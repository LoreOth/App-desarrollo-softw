from django import forms
from django.db import models
from django.conf import settings

class Zona(models.Model):
    id = models.AutoField(primary_key=True)  # ID autogenerado para la zona
    nombre = models.CharField(max_length=255)  # Nombre de la zona

    def __str__(self):
        return self.nombre
class Material(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True,  # Permite valores nulos en la base de datos
        blank=True  # Campo opcional en formularios
    )
    material = models.CharField(max_length=255)  # Nombre del material
    cantidad = models.PositiveIntegerField()  # Cantidad registrada
    cantidad_real = models.PositiveIntegerField(null=True, blank=True)  # Nueva columna opcional
    supervisado = models.BooleanField(default=False)  # Indica si el material ha sido supervisado
    id_zona = models.ForeignKey(
        Zona, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  # Hace que este campo sea opcional
        related_name='materiales'
    )  # Relación con la tabla Zona
    bonita_task = models.CharField(null=True, blank=True,max_length=255) # Tarea asociada a Bonita


    def __str__(self):
        return self.material
    
class Materiales(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del material
    cantidad_total = models.PositiveIntegerField()  # Cantidad total disponible
    costo_unitario = models.PositiveIntegerField() # Cantidad total disponible

    def __str__(self):
        return self.nombre

    
class MaterialForm(forms.ModelForm):
    material = forms.ModelChoiceField(
        queryset=Materiales.objects.all(),
        empty_label="Seleccione un material",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    id_zona = forms.ModelChoiceField(
        queryset=Zona.objects.all(),
        empty_label="Seleccione una zona",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Material
        fields = ['material', 'cantidad', 'cantidad_real', 'id_zona', 'supervisado', 'bonita_task']
