# CRM Django – Plantilla v2 (con ejemplo funcionando)

## Arrancar (1 comando)
- Linux/Mac: `bash iniciar.sh`
- Windows: `iniciar.bat`  (doble clic o ejecutarlo desde la terminal)

Abre http://127.0.0.1:8000/ · usuario **admin** · clave **admin1234**

Manual: `pip install -r requirements.txt` → `python manage.py makemigrations` → `migrate` → `cargar_ejemplo` → `runserver`.

Para recargar los datos de ejemplo desde cero: borrar`` db.sqlite3`` y ejecutar iniciar otra vez.

## Qué ya funciona
Login, panel con métricas y, en los 4 módulos (contactos, oportunidades, interacciones, tareas): listado con búsqueda, ficha, crear, editar y borrar. La ficha del contacto muestra su historial. Datos de ejemplo cargados.

## Qué haces tú
Lee **ENUNCIADO.md** y busca `TODO-ALUMNO` en el código (en VS Code: Ctrl+Shift+F).

## Mapa de archivos (por módulo)
models.py (tablas) · forms.py (formularios) · admin.py (panel /admin) · views.py (lógica) · urls.py (rutas) · templates/ (HTML)

## Cambios en el proyecto respecto a la plantilla original:

### Resumen: 
1. **AutoTaller CRM** es un CRM para un **taller mecánico de coches**: gestiona clientes, presupuestos, reparaciones, avisos y recambios.
2. Los **contactos** son las personas y empresas con las que trata el taller: clientes particulares, empresas con flota, proveedores de recambios y aseguradoras.
3. Cada contacto-cliente lleva su **matrícula** y su **vehículo** (marca y modelo) para localizarlo rápido en el mostrador.
4. Las **oportunidades** son los trabajos del taller y recorren sus etapas: Presupuesto → Aprobado → En reparación → Entregado (ganado) / Rechazado.
5. Las **interacciones** (llamadas, WhatsApp, mostrador…) y las **tareas** con prioridad (avisos de ITV, pedidos de piezas) completan el seguimiento; el módulo extra **Recambios** controla el stock.

###  LISTA DE TODOs COMPLETADOS
- **NIVEL 1 - Personalización (obligatorio)** 
    - ***TODO 0   ``settings.py``***: NOMBRE_CRM = 'AutoTaller CRM', COLOR_PRINCIPAL = ``#d35400``, LANGUAGE_CODE 'es' y TIME_ZONE 'Europe/Madrid'. Archivo TEMATICA.md (5 líneas).
    - ***TODO 1   ``contactos/models.py``:*** TIPOS = particular, empresa/flota, proveedor, aseguradora, otro.
    - ***TODO 2   ``Contacto``:*** campos propios 'matricula' y 'vehiculo' (en modelo, formulario, admin, lista y detalle).
    - ***TODO 3   ``oportunidades/models.py``:*** 5 ETAPAS (presupuesto, aprobado, en_reparacion, entregado, rechazado). La etapa "ganada" pasa a ser 'entregado' (constante Oportunidad.ETAPA_GANADA) y core/views.py se ha actualizado para que el panel siga sumando bien.
    - ***TODO 4   ``interacciones``:*** canales nuevos 'WhatsApp' y 'En mostrador'.
    - ***TODO 5   ``tareas``:*** campo 'prioridad' con choices (alta / media / baja).
    - ***TODO 10  ``cargar_ejemplo.py``:*** 10 contactos, 9 trabajos, 8 interacciones, 8 tareas y 8 recambios del taller.

- **NIVEL 2 - Ampliación (obligatorio)**
    - ***TODO 6:*** Columnas de los 4 listados ajustadas a los campos nuevos (+ listado de recambios).
    - ***TODO 7:*** Filtro por tipo en contactos y por etapa en oportunidades (desplegable + filter() en la vista). Extra: filtro por cana (interacciones), por prioridad/estado (tareas) y por categoría (recambios).
    - ***TODO 8:*** Botón "Marcar como ganada" en la ficha de la oportunidad (vista solo POST, con csrf_token).
    - ***TODO 9:*** Métricas propias en el panel: tareas vencidas (vence__lt=date.today()), coches en reparación y recambios con stock bajo.

- **NIVEL 3 - Funcionalidades CRM (elegidas 2)**
    - Importe total por etapa en oportunidades (values('etapa').annotate(Sum('importe'))).
    - Marcar tarea como hecha con un solo clic desde el listado (vista solo POST).

- **NIVEL 4 - Módulo propio (opcional)**
    - App 'recambios' (stock de piezas del taller): creada con startapp, misma estructura que 'tareas', añadida a MODULOS_CRM y visible en el menú y en el panel (tarjeta + métrica de stock bajo).

- **REGLAS DEL ENUNCIADO**  
    - Código nuevo comentado siguiendo el estilo del existente.
    - No se usa fields=``'__all__'`` en el formulario de interacciones (el autor lo asigna la vista).
    - El zip no incluye venv/ ni db.sqlite3.