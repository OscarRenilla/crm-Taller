"""
MODELOS de Contactos. Un modelo = una tabla; cada atributo = una columna.
Tras CUALQUIER cambio aquí ejecuta:
    python manage.py makemigrations     # prepara los cambios
    python manage.py migrate            # los aplica a la base de datos
(Si usas iniciar.sh / iniciar.bat, se hace solo al arrancar.)
"""
from django.db import models


class Contacto(models.Model):
    # choices: lista de pares (valor_guardado_en_BD, texto_visible). Cámbialas por las de tu temática.
    # TODO 1 (hecho): tipos de contacto propios de un taller mecánico.
    TIPOS = [
        ('particular', 'Cliente particular'),
        ('empresa', 'Empresa / flota'),
        ('proveedor', 'Proveedor de recambios'),   # OJO: el módulo recambios filtra por este valor
        ('aseguradora', 'Aseguradora'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=120)                        # Texto corto. max_length es OBLIGATORIO
    tipo = models.CharField(max_length=20, choices=TIPOS, default='particular')  # choices -> desplegable en formularios
    email = models.EmailField(blank=True)                            # blank=True -> se puede dejar vacío
    telefono = models.CharField(max_length=30, blank=True)           # Teléfono como texto (admite +34, espacios)
    notas = models.TextField(blank=True)                             # Texto largo
    creado = models.DateTimeField(auto_now_add=True)                 # auto_now_add -> fecha de creación automática
    # TODO 2 (hecho): 2 campos propios del taller.
    # Matrícula del vehículo (ej: '1234 BCD'). blank=True porque proveedores/aseguradoras no tienen coche.
    matricula = models.CharField(max_length=15, blank=True, help_text='Ej: 1234 BCD')
    # Marca y modelo del vehículo del cliente (ej: 'Seat León 1.6 TDI')
    vehiculo = models.CharField('vehículo', max_length=80, blank=True, help_text='Marca y modelo')

    class Meta:
        ordering = ['nombre']              # Orden por defecto. '-campo' = descendente

    def save(self, *args, **kwargs):
        # Guardamos la matrícula siempre en MAYÚSCULAS y sin espacios sobrantes (así el buscador es coherente)
        self.matricula = self.matricula.strip().upper()
        super().save(*args, **kwargs)      # Después guarda el objeto de forma normal

    def __str__(self):
        return self.nombre                 # Cómo se muestra el objeto en admin, desplegables, títulos


# ---------------------------------------------------------------------------
# CATÁLOGO DE CAMPOS (referencia; todo comentado)
# CharField(max_length=N) texto corto | TextField() texto largo | EmailField() | URLField()
# IntegerField() / PositiveIntegerField() enteros | FloatField() decimal aproximado (no para dinero)
# DecimalField(max_digits=10, decimal_places=2) dinero | BooleanField(default=False) sí/no
# DateField() fecha | DateTimeField() fecha y hora | ImageField(upload_to='fotos/') (necesita Pillow)
# Opciones: null=True (BD admite vacío) · blank=True (formulario admite vacío) · default=valor
#           unique=True (sin repetidos) · choices=[(valor, 'Texto')] · verbose_name='Etiqueta'
#           help_text='Ayuda' · auto_now_add=True (fecha al crear) · auto_now=True (fecha al guardar)
# Relaciones: ForeignKey(Modelo, on_delete=..., related_name='x') muchos-a-uno
#             ManyToManyField(Modelo, blank=True) muchos-a-muchos | OneToOneField(Modelo, on_delete=...) uno-a-uno
# on_delete: CASCADE | PROTECT | SET_NULL (con null=True) | SET_DEFAULT | DO_NOTHING
# ---------------------------------------------------------------------------
