"""
VISTAS de Recambios: reciben una petición del navegador (request)
y devuelven una respuesta, como una página HTML o una redirección.
CRUD significa crear, leer, actualizar y borrar.
"""

# Permite mostrar avisos temporales, por ejemplo «Guardado correctamente».
from django.contrib import messages

# Hace que solo puedan acceder usuarios que hayan iniciado sesión.
from django.contrib.auth.decorators import login_required

# Permite combinar condiciones con "O" en una búsqueda (Q(a) | Q(b)).
from django.db.models import Q

# Herramientas para mostrar páginas, buscar objetos y redirigir.
from django.shortcuts import render, get_object_or_404, redirect

# Función del proyecto que prepara los campos de un objeto para mostrarlos.
from core.utils import campos_de

# Importa el modelo y el formulario de recambios.
from .models import Recambio
from .forms import RecambioForm


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def index(request):
    """Muestra el listado, con búsqueda (?q=) y filtro por categoría (?categoria=)."""

    # Lee los parámetros de la URL. Si no existen, usa texto vacío.
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '')

    # Obtiene todos los recambios; select_related('proveedor') trae el proveedor en la misma consulta.
    objetos = Recambio.objects.select_related('proveedor')

    # Si se escribió algo, busca por nombre O por referencia (Q permite el "O").
    if q:
        objetos = objetos.filter(Q(nombre__icontains=q) | Q(referencia__icontains=q))

    # Filtro por categoría (desplegable del listado).
    if categoria:
        objetos = objetos.filter(categoria=categoria)

    # Carga la plantilla del listado y le entrega los datos que necesita.
    return render(
        request,
        'recambios/lista.html',
        {'objetos': objetos, 'q': q, 'categoria': categoria, 'categorias': Recambio.CATEGORIAS}
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def detalle(request, pk):
    """Muestra la ficha de un recambio. pk es su identificador."""

    # Busca el recambio; si no existe, muestra un error 404 («no encontrado»).
    objeto = get_object_or_404(Recambio, pk=pk)

    # Muestra la plantilla de detalle genérica del proyecto.
    return render(
        request,
        'core/detalle.html',
        {'objeto': objeto, 'campos': campos_de(objeto), 'ns': 'recambios'}
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def crear(request):
    """GET muestra el formulario; POST procesa los datos enviados."""

    # Si todavía no se ha enviado, None permite mostrar el formulario vacío.
    form = RecambioForm(request.POST or None)

    # Comprueba que se haya enviado con POST y que los datos sean válidos.
    if request.method == 'POST' and form.is_valid():

        # Guarda el nuevo recambio en la base de datos.
        obj = form.save()

        # Añade un aviso de éxito.
        messages.success(request, 'Creado correctamente')

        # Lleva al usuario a la ficha del recambio recién creado.
        return redirect('recambios:detalle', pk=obj.pk)

    # Si no se envió o tiene errores, muestra el formulario.
    return render(
        request,
        'core/form.html',
        {'form': form, 'titulo': 'Nuevo: recambio', 'volver': 'recambios:index'}
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def editar(request, pk):
    """Muestra y procesa el formulario para editar un recambio existente."""

    # Busca el recambio que se quiere editar; si no existe, error 404.
    objeto = get_object_or_404(Recambio, pk=pk)

    # instance=objeto indica que se actualizará ese recambio, no se creará otro.
    form = RecambioForm(request.POST or None, instance=objeto)

    # Si se envió el formulario y todos los datos son válidos:
    if request.method == 'POST' and form.is_valid():

        # Guarda los cambios.
        form.save()

        # Aviso de éxito.
        messages.success(request, 'Cambios guardados')

        # Redirige a la ficha del recambio editado.
        return redirect('recambios:detalle', pk=objeto.pk)

    # Muestra el formulario de edición (con errores si los hay).
    return render(
        request,
        'core/form.html',
        {'form': form, 'titulo': f'Editar: {objeto}', 'volver': 'recambios:index'}
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def borrar(request, pk):
    """GET muestra la confirmación; POST realiza el borrado."""

    # Busca el recambio que se quiere borrar; si no existe, error 404.
    objeto = get_object_or_404(Recambio, pk=pk)

    # Solo borra cuando recibe una petición POST (al confirmar el formulario).
    if request.method == 'POST':

        # Elimina el recambio de la base de datos.
        objeto.delete()

        # Aviso de que se eliminó.
        messages.success(request, 'Eliminado')

        # Vuelve al listado.
        return redirect('recambios:index')

    # Si no es POST, muestra la página que pide confirmar el borrado.
    return render(
        request,
        'core/confirmar_borrado.html',
        {'objeto': objeto, 'volver': 'recambios:index'}
    )
