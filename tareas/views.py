"""
VISTAS de Tareas: reciben una petición del navegador (request)
y devuelven una respuesta, como una página HTML o una redirección.
CRUD significa crear, leer, actualizar y borrar.
"""

# Permite mostrar avisos temporales, por ejemplo «Guardado correctamente».
from django.contrib import messages

# Hace que solo puedan acceder usuarios que hayan iniciado sesión.
from django.contrib.auth.decorators import login_required

# Fecha de hoy, para resaltar las tareas vencidas.
from datetime import date

# Decorador que solo permite peticiones POST (con GET responde "405 método no permitido").
from django.views.decorators.http import require_POST

# Herramientas para mostrar páginas, buscar objetos y redirigir.
from django.shortcuts import render, get_object_or_404, redirect

# Función del proyecto que prepara los campos de un objeto para mostrarlos.
from core.utils import campos_de

# Importa el modelo y el formulario de tareas.
from .models import Tarea
from .forms import TareaForm


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def index(request):
    """Muestra el listado de tareas y permite buscar: /tareas/?q=texto."""

    # Lee el parámetro q de la URL. Si no existe, usa texto vacío.
    # strip() quita espacios sobrantes al principio y al final.
    q = request.GET.get('q', '').strip()

    # Obtiene todas las tareas de la base de datos.
    objetos = Tarea.objects.all()

    # Si se escribió algo en la búsqueda, filtra las tareas.
    if q:
        # Busca títulos que contengan q, sin distinguir mayúsculas y minúsculas.
        objetos = objetos.filter(titulo__icontains=q)

    # TODO 7 (extra, hecho): filtro por prioridad (campo con opciones).
    prioridad = request.GET.get('prioridad', '')
    if prioridad:
        # WHERE prioridad = 'alta'
        objetos = objetos.filter(prioridad=prioridad)

    # Filtro por estado: solo pendientes o solo hechas (si llega vacío, se enseñan todas).
    estado = request.GET.get('estado', '')
    if estado == 'pendientes':
        objetos = objetos.filter(hecha=False)
    elif estado == 'hechas':
        objetos = objetos.filter(hecha=True)

    # Carga la plantilla del listado y le entrega los datos que necesita:
    # objetos = tareas; q/prioridad/estado = filtros elegidos; prioridades = opciones del desplegable;
    # hoy = fecha actual (la plantilla la compara con "vence" para marcar las vencidas en rojo).
    return render(
        request,
        'tareas/lista.html',
        {
            'objetos': objetos,
            'q': q,
            'prioridad': prioridad,
            'prioridades': Tarea.PRIORIDADES,
            'estado': estado,
            'hoy': date.today(),
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def detalle(request, pk):
    """Muestra la ficha de una tarea. pk es su identificador."""

    # Busca la tarea con el identificador recibido en la URL.
    # Si no existe, muestra un error 404 («no encontrado»).
    objeto = get_object_or_404(Tarea, pk=pk)

    # Muestra la plantilla de detalle y le pasa la tarea,
    # sus campos preparados para mostrarse y el nombre de la aplicación.
    return render(
        request,
        'core/detalle.html',
        {
            'objeto': objeto,
            'campos': campos_de(objeto),
            'ns': 'tareas'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def crear(request):
    """GET muestra el formulario; POST procesa los datos enviados."""

    # request.POST contiene los datos enviados por el formulario.
    # Si todavía no se ha enviado, None permite mostrar el formulario vacío.
    # initial precarga el contacto indicado en la URL, si lo hay.
    form = TareaForm(
        request.POST or None,
        initial={'contacto': request.GET.get('contacto')}
    )

    # Comprueba que el usuario haya enviado el formulario con POST
    # y que sus datos sean válidos.
    if request.method == 'POST' and form.is_valid():

        # Guarda la nueva tarea en la base de datos.
        obj = form.save()

        # Añade un aviso de que la tarea se creó correctamente.
        messages.success(request, 'Creado correctamente')

        # Lleva al usuario a la ficha de la tarea recién creada.
        # Redirigir después de guardar evita repetir el envío al recargar.
        return redirect('tareas:detalle', pk=obj.pk)

    # Si aún no se envió el formulario o tiene errores, muestra la página
    # del formulario junto con su título y el enlace para volver al listado.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': 'Nuevo: tarea',
            'volver': 'tareas:index'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def editar(request, pk):
    """Muestra y procesa el formulario para editar una tarea existente."""

    # Busca la tarea que se quiere editar; si no existe, devuelve un error 404.
    objeto = get_object_or_404(Tarea, pk=pk)

    # Crea un formulario con los datos enviados, si los hay.
    # instance=objeto indica que se actualizará esa tarea, no se creará otra.
    form = TareaForm(request.POST or None, instance=objeto)

    # Si se envió el formulario y todos los datos son válidos:
    if request.method == 'POST' and form.is_valid():

        # Guarda los cambios de la tarea existente.
        form.save()

        # Añade un aviso de que los cambios se guardaron.
        messages.success(request, 'Cambios guardados')

        # Redirige a la ficha de la tarea editada.
        return redirect('tareas:detalle', pk=objeto.pk)

    # Muestra el formulario de edición. Si hay errores, también aparecen aquí.
    # La f-string inserta la tarea en el texto del título.
    return render(
        request,
        'core/form.html',
        {
            'form': form,
            'titulo': f'Editar: {objeto}',
            'volver': 'tareas:index'
        }
    )


# Protege esta vista: solo pueden verla usuarios con sesión iniciada.
@login_required
def borrar(request, pk):
    """GET muestra la confirmación; POST realiza el borrado."""

    # Busca la tarea que se quiere borrar; si no existe, devuelve un error 404.
    objeto = get_object_or_404(Tarea, pk=pk)

    # Solo borra cuando recibe una petición POST, normalmente al confirmar
    # el formulario. Abrir la página con GET no elimina nada.
    if request.method == 'POST':

        # Elimina la tarea de la base de datos.
        objeto.delete()

        # Añade un aviso de que se eliminó correctamente.
        messages.success(request, 'Eliminado')

        # Redirige al listado de tareas.
        return redirect('tareas:index')

    # Si la petición no es POST, muestra la página que pide confirmar el borrado.
    return render(
        request,
        'core/confirmar_borrado.html',
        {
            'objeto': objeto,
            'volver': 'tareas:index'
        }
    )


# NIVEL 3 (hecho): marcar una tarea como hecha con un solo clic desde el listado.
# Solo acepta POST (el botón del listado es un formulario), así que no se puede activar por error con un enlace.
@login_required
@require_POST
def marcar_hecha(request, pk):
    """Pone hecha=True en la tarea y vuelve al listado."""

    # Busca la tarea; si no existe, error 404.
    objeto = get_object_or_404(Tarea, pk=pk)

    # Marca la tarea como hecha y guarda el cambio.
    objeto.hecha = True
    objeto.save()

    # Aviso de éxito para la siguiente página.
    messages.success(request, f'Tarea «{objeto}» marcada como hecha')

    # Vuelve al listado de tareas.
    return redirect('tareas:index')
