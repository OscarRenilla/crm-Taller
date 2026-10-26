"""
FORMULARIOS: un ModelForm crea un formulario a partir de un modelo
y aprovecha sus campos y validaciones.
"""

# Importa las herramientas para crear formularios de Django.
from django import forms

# Importa el modelo Recambio, cuyos datos tendrá el formulario.
from .models import Recambio


# Crea un formulario basado en el modelo Recambio.
class RecambioForm(forms.ModelForm):

    # Clase especial donde se configura este ModelForm.
    class Meta:

        # Indica qué modelo se usará para crear el formulario.
        model = Recambio

        # Indica qué campos del modelo aparecerán en el formulario.
        fields = ['referencia', 'nombre', 'categoria', 'proveedor', 'precio', 'stock', 'stock_minimo']
