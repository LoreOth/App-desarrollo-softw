from rest_framework import serializers
from .forms import Materiales

class MaterialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiales
        fields = ['id', 'nombre', 'cantidad_total', 'costo_unitario']
