"""
MODELOS de Recambios (módulo propio, Nivel 4). Un modelo representa una tabla de la base de datos;
cada campo del modelo representa una columna.
Tras cambiar el modelo, ejecuta:
    python manage.py makemigrations  # Prepara una migración con los cambios.
    python manage.py migrate         # Aplica los cambios a la base de datos.
(Si usas iniciar.sh / iniciar.bat, estos comandos se ejecutan al arrancar.)
"""

# Importa las herramientas para definir modelos y campos de base de datos.
from django.db import models


# Define el modelo Recambio: una pieza o consumible que el taller tiene (o debe tener) en el almacén.
class Recambio(models.Model):

    # Opciones del campo "categoria".
    # El primer valor se guarda en la base de datos; el segundo se muestra en pantalla.
    CATEGORIAS = [
        ('motor', 'Motor'),
        ('frenos', 'Frenos'),
        ('filtros', 'Filtros y aceites'),
        ('electrico', 'Eléctrico'),
        ('neumaticos', 'Neumáticos'),
        ('otros', 'Otros'),
    ]

    # Referencia del fabricante o del proveedor. unique=True impide repetirla en dos recambios.
    referencia = models.CharField(max_length=40, unique=True)

    # Nombre descriptivo de la pieza.
    nombre = models.CharField(max_length=150)

    # Categoría de la pieza, limitada a las opciones de CATEGORIAS.
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='otros')

    # Proveedor al que se compra la pieza (un contacto de tipo "proveedor").
    # SET_NULL conserva el recambio si se borra el proveedor; para eso hacen falta null=True y blank=True.
    # limit_choices_to hace que en el formulario solo salgan contactos de tipo 'proveedor'.
    # related_name permite consultar los recambios de un proveedor así: contacto.recambios.all()
    proveedor = models.ForeignKey(
        'contactos.Contacto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'tipo': 'proveedor'},
        related_name='recambios'
    )

    # Precio de venta por unidad. DecimalField es el adecuado para dinero (nunca FloatField).
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Unidades que hay ahora mismo en el almacén. PositiveIntegerField no admite negativos.
    stock = models.PositiveIntegerField(default=0)

    # Por debajo (o igual) de esta cantidad el recambio se considera "stock bajo" y hay que reponerlo.
    stock_minimo = models.PositiveIntegerField(default=2)

    # Configuración adicional del modelo.
    class Meta:

        # Ordena alfabéticamente por nombre.
        ordering = ['nombre']

        # Nombre plural que Django muestra en el panel de administración.
        verbose_name_plural = 'recambios'

    # Propiedad calculada (no es una columna): True si hay que reponer el recambio.
    # Se usa en plantillas así: {% if o.stock_bajo %}
    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    # Cómo se representa un recambio como texto (admin, desplegables, títulos).
    def __str__(self):
        return f'{self.nombre} ({self.referencia})'
