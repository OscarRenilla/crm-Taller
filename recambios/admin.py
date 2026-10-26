"""
ADMIN: configuración para gestionar datos desde /admin/
sin tener que crear vistas propias.
"""

# Importa las herramientas del sitio de administración de Django.
from django.contrib import admin

# Importa el modelo Recambio que se quiere administrar.
from .models import Recambio


# Registra Recambio en el administrador y le asigna esta configuración.
@admin.register(Recambio)
class RecambioAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el listado de recambios.
    list_display = ('referencia', 'nombre', 'categoria', 'proveedor', 'precio', 'stock', 'stock_minimo',)

    # Filtro lateral por categoría.
    list_filter = ('categoria',)

    # Caja de búsqueda por referencia, nombre y nombre del proveedor.
    search_fields = ('referencia', 'nombre', 'proveedor__nombre',)
