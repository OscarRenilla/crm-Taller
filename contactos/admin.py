"""
ADMIN: gestión rápida de datos en /admin/ sin escribir vistas.
"""
from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'matricula', 'vehiculo', 'email', 'telefono',)        # Columnas del listado (TODO 2: matricula y vehiculo)
    list_filter = ('tipo',)        # Filtros laterales
    search_fields = ('nombre', 'email', 'matricula', 'vehiculo',)       # Caja de búsqueda ('^campo' empieza por · '=campo' exacto · 'relacion__campo')
    # Más opciones: ordering = (...) · list_editable = ('campo',) · date_hierarchy = 'fecha' · readonly_fields = (...)
