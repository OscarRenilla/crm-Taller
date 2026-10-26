"""Define las direcciones web de la sección de recambios.
Se montan bajo /recambios/ desde crm_project/urls.py.
"""

# Importa la función path para conectar direcciones web con vistas.
from django.urls import path

# Importa las vistas de esta aplicación.
from . import views


# Nombre de esta aplicación. Sirve para referirse a sus rutas
# por nombre, por ejemplo: {% url 'recambios:index' %}.
app_name = 'recambios'


# Lista de rutas de la aplicación.
urlpatterns = [
    # La ruta vacía corresponde a /recambios/ y muestra el listado.
    path('', views.index, name='index'),

    # /recambios/nuevo/ muestra el formulario para crear un recambio.
    path('nuevo/', views.crear, name='crear'),

    # <int:pk> captura un número entero de la dirección y lo pasa a la vista como pk.
    path('<int:pk>/', views.detalle, name='detalle'),

    # /recambios/3/editar/ abre el formulario para editar el recambio 3.
    path('<int:pk>/editar/', views.editar, name='editar'),

    # /recambios/3/borrar/ abre la página para borrar el recambio 3.
    path('<int:pk>/borrar/', views.borrar, name='borrar'),
]
