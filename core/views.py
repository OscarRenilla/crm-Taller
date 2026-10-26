from datetime import date                      # date.today() = fecha de hoy (para detectar tareas vencidas)
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum            # Sum = suma de una columna | F('campo') = "el valor de otra columna"
from django.shortcuts import render

def _modelo(app, nombre):
    """Devuelve el modelo o None si el módulo está desactivado en MODULOS_CRM (así el panel no se rompe)."""
    try:
        return apps.get_model(app, nombre)
    except LookupError:
        return None

@login_required   # Sin sesión iniciada -> redirige al login
def inicio(request):
    # Tarjetas con el número de objetos de cada módulo activo
    resumen = []
    for app, modelo, etiqueta in [('contactos', 'Contacto', 'Contactos'),
                                  ('oportunidades', 'Oportunidad', 'Oportunidades'),
                                  ('interacciones', 'Interaccion', 'Interacciones'),
                                  ('tareas', 'Tarea', 'Tareas'),
                                  ('recambios', 'Recambio', 'Recambios')]:   # Módulo propio (Nivel 4)
        M = _modelo(app, modelo)
        if M:
            resumen.append({'etiqueta': etiqueta, 'n': M.objects.count(), 'url': f'{app}:index'})

    # None = "módulo desactivado": la plantilla no enseña esa métrica
    ultimas, pendientes, ganado = [], None, None
    vencidas, en_reparacion, stock_bajo = None, None, None
    Inter = _modelo('interacciones', 'Interaccion')
    if Inter:
        ultimas = Inter.objects.select_related('contacto')[:5]      # Últimas 5 (el modelo ya ordena por -fecha)
    Tarea = _modelo('tareas', 'Tarea')
    if Tarea:
        pendientes = Tarea.objects.filter(hecha=False).count()      # filter(campo=valor) = WHERE
        # TODO 9 (hecho): métrica propia -> tareas VENCIDAS = sin hacer y con fecha límite anterior a hoy.
        # vence__lt = "less than" (menor que); date.today() = hoy.
        vencidas = Tarea.objects.filter(hecha=False, vence__lt=date.today()).count()
    Op = _modelo('oportunidades', 'Oportunidad')
    if Op:
        # TODO 3 (hecho): la etapa "ganada" ahora se llama 'entregado'. En vez de escribirla a mano
        # usamos la constante del modelo (Op.ETAPA_GANADA), así el panel siempre suma bien aunque se renombre.
        ganado = Op.objects.filter(etapa=Op.ETAPA_GANADA).aggregate(t=Sum('importe'))['t'] or 0   # Sum = suma de la columna
        # TODO 9 (hecho): segunda métrica propia -> coches que están ahora mismo dentro del taller.
        en_reparacion = Op.objects.filter(etapa=Op.ETAPA_EN_REPARACION).count()
    Recambio = _modelo('recambios', 'Recambio')
    if Recambio:
        # TODO 9 + NIVEL 4 (hecho): recambios con stock bajo = stock menor o igual que su stock mínimo.
        # F('stock_minimo') compara dos columnas de la misma fila (no un número fijo).
        stock_bajo = Recambio.objects.filter(stock__lte=F('stock_minimo')).count()

    return render(request, 'core/inicio.html', {
        'resumen': resumen, 'ultimas': ultimas, 'pendientes': pendientes, 'ganado': ganado,
        'vencidas': vencidas, 'en_reparacion': en_reparacion, 'stock_bajo': stock_bajo})
