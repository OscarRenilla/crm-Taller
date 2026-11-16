# 🛡️ GUÍA DEFINITIVA PARA LA DEFENSA DEL PROYECTO: AutoTaller CRM
> **Proyecto:** Adaptación y Ampliación de un CRM en Django  
> **Temática:** Taller Mecánico de Automóviles y Gestión de Flotas  
> **Nombre del Sistema:** AutoTaller CRM  
> **Stack Técnico:** Python 3, Django 4.2+, SQLite3, HTML5/CSS3 nativo  

---

## 📌 ÍNDICE DE CONTENIDOS
1. [Discurso Inicial de 1 Minuto (Elevator Pitch)](#1-discurso-inicial-de-1-minuto-elevator-pitch)
2. [Ficha Técnica y Mapa Conceptual del Negocio](#2-ficha-técnica-y-mapa-conceptual-del-negocio)
3. [Arquitectura y Estructura del Software (MVT y Modularidad)](#3-arquitectura-y-estructura-del-software-mvt-y-modularidad)
4. [Resumen Exhaustivo de Requisitos Implementados (Niveles 1 al 4)](#4-resumen-exhaustivo-de-requisitos-implementados-niveles-1-al-4)
5. [Decisiones Técnicas Notables y Buenas Prácticas (Para lucirse)](#5-decisiones-técnicas-notables-y-buenas-prácticas-para-lucirse)
6. [Batería de Preguntas y Respuestas: De lo Más Simple a lo Más Complejo](#6-batería-de-preguntas-y-respuestas-de-lo-más-simple-a-lo-más-complejo)
   - [Bloque A: Fundamentos Básicos y Entorno](#bloque-a-fundamentos-básicos-y-entorno)
   - [Bloque B: Modelos, Formularios y Base de Datos](#bloque-b-modelos-formularios-y-base-de-datos)
   - [Bloque C: Vistas, Lógica de Negocio y Seguridad](#bloque-c-vistas-lógica-de-negocio-y-seguridad)
   - [Bloque D: Consultas Avanzadas ORM y Agregaciones](#bloque-d-consultas-avanzadas-orm-y-agregaciones)
   - [Bloque E: Arquitectura, Escalabilidad y Nivel Experto](#bloque-e-arquitectura-escalabilidad-y-nivel-experto)
7. [Guión de Demostración en Vivo (Paso a Paso en 3 Minutos)](#7-guión-de-demostración-en-vivo-paso-a-paso-en-3-minutos)
8. [Chuleta de Comandos Rápidos por si Te Piden Probar en Vivo](#8-chuleta-de-comandos-rápidos-por-si-te-piden-probar-en-vivo)

---

## 1. DISCURSO INICIAL DE 1 MINUTO (ELEVATOR PITCH)

> *"Buenos días / tardes. He adaptado y ampliado este CRM para convertirlo en **AutoTaller CRM**, una plataforma de gestión integral especializada para talleres mecánicos de automóviles.*
>
> *El software centraliza todo el ciclo de vida del taller: desde que un cliente entra por el mostrador o nos contacta por WhatsApp, registrando su **matrícula y modelo de vehículo**, pasando por la emisión de presupuestos, el seguimiento de los coches que están **en reparación**, hasta la entrega y cobro del trabajo marcado como ganado.*
>
> *Además de cumplir con todos los requerimientos obligatorios (personalización, filtros avanzados, acciones rápidas seguras por POST y métricas en tiempo real), he implementado dos funcionalidades CRM avanzadas: el **análisis de facturación agrupado por etapa mediante agregaciones del ORM**, y el **marcado rápido de tareas pendientes con un solo clic**.*
>
> *Finalmente, como ampliación modular (Nivel 4), he desarrollado desde cero la app **Recambios**, que controla el stock de piezas del almacén, vincula cada pieza a proveedores reales y avisa mediante alertas visuales en el panel cuando es necesario reponer material utilizando comparaciones de columnas a nivel de base de datos.*
>
> *Todo el código ha sido documentado exhaustivamente, aplicando buenas prácticas de Django como la protección CSRF, consultas optimizadas con `select_related` para evitar consultas N+1, y el patrón Post-Redirect-Get."*

---

## 2. FICHA TÉCNICA Y MAPA CONCEPTUAL DEL NEGOCIO

### ¿Por qué esta temática y cómo encaja en un CRM?
Un taller mecánico no gestiona "contactos genéricos", sino propietarios y vehículos asociados que requieren mantenimiento continuo, avisos periódicos de ITV, pedidos urgentes de piezas a proveedores y liquidaciones con aseguradoras.

| Entidad del CRM | Concepto en el Taller | Particularidad Técnica |
|---|---|---|
| **Contactos** | Clientes particulares, flotas de empresas, proveedores de piezas y aseguradoras peritadoras. | Incluye `matricula` y `vehiculo`. La matrícula se normaliza automáticamente a mayúsculas (`save()`). |
| **Oportunidades** | Trabajos de reparación y mantenimiento (ej. "Cambio embrague", "Revisión pre-ITV"). | 5 etapas: `Presupuesto`, `Aprobado`, `En reparación`, `Entregado (ganado)` y `Rechazado`. |
| **Interacciones** | Canales de comunicación taller-cliente. | Nuevos canales: `WhatsApp` (clave para enviar presupuestos en PDF o avisar de fin de trabajo) y `En mostrador`. Asigna autor automáticamente con `request.user`. |
| **Tareas** | Avisos de vencimiento, pedidos a proveedores, llamadas de ITV o cobros pendientes. | Campo `prioridad` (`alta`, `media`, `baja`). Detección automática de tareas vencidas (`vence < hoy`). |
| **Recambios** *(App Propia)* | Stock de piezas en almacén (filtros, discos, aceites, baterías...). | Relación con proveedor (`limit_choices_to={'tipo': 'proveedor'}`). Propiedad `stock_bajo` si `stock <= stock_minimo`. |

---

## 3. ARQUITECTURA Y ESTRUCTURA DEL SOFTWARE (MVT Y MODULARIDAD)

Django utiliza el patrón arquitectónico **MVT (Model - View - Template)**:

```
[ Navegador del Usuario ]
         │  petición HTTP (GET / POST)
         ▼
[ urls.py (Enrutador) ] ──────────► Dirige la URL a la función correspondiente
         │
         ▼
[ views.py (Lógica / Controlador) ]
    ├──► Consulta / Modifica ──► [ models.py (Capa de Datos - ORM) ] ──► [ SQLite3 ]
    ├──► Valida datos con    ──► [ forms.py (ModelForm) ]
    └──► Renderiza datos en  ──► [ templates/*.html (Presentación) ]
         │
         ▼  respuesta HTML con datos
[ Pantalla del Usuario ]
```

### Modularidad Dinámica del Proyecto:
1. **`settings.MODULOS_CRM`**: Lista los módulos activos: `['contactos', 'oportunidades', 'interacciones', 'tareas', 'recambios']`.
2. **`core.context_processors.crm`**: Inyecta automáticamente en **todas las plantillas** las variables `{{ NOMBRE_CRM }}`, `{{ COLOR }}` y el menú `{{ modulos }}`. Si añades o quitas un módulo en `settings.py`, el menú de navegación se actualiza automáticamente sin tocar el HTML.
3. **`crm_project/urls.py`**: Itera dinámicamente sobre `MODULOS_CRM` mediante `urlpatterns.append(path(f'{modulo}/', include(f'{modulo}.urls')))`.

---

## 4. RESUMEN EXHAUSTIVO DE REQUISITOS IMPLEMENTADOS (NIVELES 1 AL 4)

### 🔹 NIVEL 1: Personalización (Obligatorio - 3 Puntos)
- **TODO 0 (Configuración general):** 
  - `NOMBRE_CRM = 'AutoTaller CRM'`
  - `COLOR_PRINCIPAL = '#d35400'` (naranja mecánico corporativo)
  - `LANGUAGE_CODE = 'es'`, `TIME_ZONE = 'Europe/Madrid'`.
- **TODO 1 (Tipos de contacto):**
  - Opciones adaptadas: `particular` (Cliente particular), `empresa` (Empresa / flota), `proveedor` (Proveedor de recambios), `aseguradora`, `otro`.
- **TODO 2 (Campos propios en Contacto):**
  - `matricula` (`CharField(max_length=15, blank=True)`).
  - `vehiculo` (`CharField('vehículo', max_length=80, blank=True)`).
  - Integrados en: modelo (`save()` con `.strip().upper()`), `ContactoForm`, `ContactoAdmin` (`list_display`, `search_fields`), `lista.html` (columnas visibles) y `detalle.html` (`campos_de`).
- **TODO 3 (Etapas de Oportunidad):**
  - 5 etapas del ciclo del taller: `presupuesto`, `aprobado`, `en_reparacion`, `entregado` (ganado), `rechazado`.
  - Constantes de clase para robustez: `ETAPA_GANADA = 'entregado'` y `ETAPA_EN_REPARACION = 'en_reparacion'`.
  - Sincronización en `core/views.py`: el panel suma la facturación usando `Op.ETAPA_GANADA`.
- **TODO 4 (Canales en Interacciones):**
  - Incorporados `whatsapp` ('WhatsApp') y `mostrador` ('En mostrador').
- **TODO 5 (Prioridad en Tareas):**
  - Añadido campo `prioridad` con choices (`alta`, `media`, `baja`), por defecto `media`.
- **TODO 10 (Datos de prueba temáticos en `cargar_ejemplo.py`):**
  - Carga automática con `BaseCommand`: 10 contactos con matrículas y modelos reales, 9 trabajos (reparaciones en diferentes etapas), 8 interacciones con los canales nuevos, 8 tareas con fechas dinámicas relativas a hoy (`date.today() ± días`), y 8 recambios con stocks y precios reales.

---

### 🔸 NIVEL 2: Ampliación (Obligatorio - 3 Puntos)
- **TODO 6 (Ajuste de columnas en listados):**
  - Listado de contactos: columnas Matrícula y Vehículo añadidas.
  - Listado de oportunidades: columna Cierre previsto.
  - Listado de tareas: columna Prioridad y aviso en rojo para tareas vencidas.
  - Listado de recambios: referencia, stock y aviso visual de reponer.
- **TODO 7 (Filtros y Búsquedas avanzadas):**
  - **Contactos:** Filtro por `tipo` (`?tipo=...`) y búsqueda multi-campo con objetos `Q`:  
    `Q(nombre__icontains=q) | Q(matricula__icontains=q) | Q(vehiculo__icontains=q)`.
  - **Oportunidades:** Filtro por `etapa` (`?etapa=...`) y búsqueda por trabajo, cliente o matrícula:  
    `Q(titulo__icontains=q) | Q(contacto__nombre__icontains=q) | Q(contacto__matricula__icontains=q)`.
  - **Interacciones:** Filtro extra por `canal`.
  - **Tareas:** Filtro extra por `prioridad` y por `estado` (`pendientes` / `hechas`).
  - **Recambios:** Filtro extra por `categoria`.
- **TODO 8 (Acción "Marcar como ganada" en Oportunidad):**
  - Vista dedicada `marcar_ganada(request, pk)`.
  - Protegida con `@login_required` y `@require_POST` (no se puede alterar mediante una petición GET accidental o maliciosa).
  - En la plantilla `oportunidades/detalle.html`: formulario con `{% csrf_token %}` y botón que solo aparece si la oportunidad no está ganada (`{% if not ya_ganada %}`).
- **TODO 9 (Métricas personalizadas en el Dashboard):**
  - **Tareas vencidas:** `Tarea.objects.filter(hecha=False, vence__lt=date.today()).count()` (se resalta en color rojo `#c0392b` si es mayor a 0).
  - **Coches en taller:** `Op.objects.filter(etapa=Op.ETAPA_EN_REPARACION).count()`.
  - **Recambios con stock bajo:** `Recambio.objects.filter(stock__lte=F('stock_minimo')).count()` (utiliza la expresión `F` de Django).

---

### 🚀 NIVEL 3: Funcionalidades CRM Avanzadas (Elegidas 2 - 2 Puntos)
1. **Importe total por etapa en Oportunidades:**
   - Implementado en `oportunidades/views.py`:
     ```python
     agrupado = {
         fila['etapa']: fila
         for fila in Oportunidad.objects.values('etapa').annotate(total=Sum('importe'), n=Count('id'))
     }
     ```
   - Construye una tabla resumen visible en `oportunidades/lista.html` que muestra para cada etapa: nombre, número de trabajos y suma acumulada en euros, garantizando que aparezcan todas las etapas incluso si tienen 0 trabajos.
2. **Marcar tarea como hecha con un solo clic desde el listado:**
   - Implementado en `tareas/views.py` (`marcar_hecha(request, pk)`) con `@require_POST`.
   - En `tareas/lista.html`: botón inline `✔ Hecha` dentro de un `<form method="post">` con `{% csrf_token %}`, presente exclusivamente en las tareas pendientes.

---

### 🌟 NIVEL 4: Módulo Propio (+1 Punto Extra)
- Creación de la aplicación **`recambios`** (almacén de repuestos del taller):
  - Modelo `Recambio` con `referencia` (única), `nombre`, `categoria` (choices), `precio` (`DecimalField`), `stock` y `stock_minimo` (`PositiveIntegerField`).
  - Relación inteligente: `proveedor = models.ForeignKey('contactos.Contacto', limit_choices_to={'tipo': 'proveedor'}, on_delete=models.SET_NULL, null=True, blank=True)`.
  - Propiedad calculada en modelo: `@property def stock_bajo(self): return self.stock <= self.stock_minimo`.
  - CRUD completo (listar con búsqueda y filtro de categoría, ver detalle, crear, editar y borrar).
  - Integración en `MODULOS_CRM`, en el menú de cabecera y en las métricas de control de stock del Dashboard.

---

## 5. DECISIONES TÉCNICAS NOTABLES Y BUENAS PRÁCTICAS (PARA LUCIRSE)

Si te preguntan por qué has programado algo de una forma concreta, saca a relucir estos 7 puntos clave:

1. **Evitar consultas N+1 con `select_related()`:**
   En `oportunidades/views.py` y `recambios/views.py`, en lugar de hacer `Oportunidad.objects.all()`, se hace:
   ```python
   objetos = Oportunidad.objects.select_related('contacto')
   ```
   *Explicación:* Realiza un `SQL JOIN` en una única consulta a la base de datos en lugar de lanzar una consulta adicional por cada fila que se dibuja en la tabla HTML.

2. **Comparación a nivel de base de datos con `F()` expressions:**
   En `core/views.py`:
   ```python
   stock_bajo = Recambio.objects.filter(stock__lte=F('stock_minimo')).count()
   ```
   *Explicación:* `F('stock_minimo')` permite comparar dos columnas de la misma tabla en la cláusula `WHERE` del motor SQL sin necesidad de traer todos los registros a la memoria de Python.

3. **Asignación segura del autor con `commit=False`:**
   En `interacciones/views.py`:
   ```python
   obj = form.save(commit=False)
   obj.autor = request.user
   obj.save()
   ```
   *Explicación:* Cumple estrictamente la regla del enunciado de no usar `fields='__all__'`. El usuario logueado se asocia en el backend garantizando que ningún usuario malintencionado pueda suplantar la autoría mediante manipulación del formulario HTML.

4. **Patrón Post-Redirect-Get (PRG):**
   Tras procesar con éxito un formulario POST (crear, editar, marcar ganada o marcar tarea hecha), la vista responde siempre con un `redirect()`. Esto impide que si el usuario pulsa F5 en su navegador se reenvíe la petición y se dupliquen registros.

5. **Seguridad contra ataques CSRF y manipulación de estado:**
   Las acciones que modifican el estado (`marcar_ganada` y `marcar_hecha`) están decoradas con `@require_POST` y se ejecutan desde etiquetas `<form method="post">` con `{% csrf_token %}`. Si un atacante intenta invocar la URL por enlace GET (ej. `<a href="/tareas/1/hecha/">`), el servidor rechaza la petición con un código HTTP 405 (Method Not Allowed).

6. **Normalización de datos en el ciclo de vida del modelo:**
   En `contactos/models.py`:
   ```python
   def save(self, *args, **kwargs):
       self.matricula = self.matricula.strip().upper()
       super().save(*args, **kwargs)
   ```
   *Explicación:* Garantiza que las matrículas se almacenen siempre en mayúsculas y limpias de espacios accidentales, facilitando búsquedas exactas e indexación coherente.

7. **Uso de `DecimalField` frente a `FloatField`:**
   Tanto en `Oportunidad.importe` como en `Recambio.precio` se utiliza `DecimalField(max_digits=..., decimal_places=2)`. Los números en coma flotante (`FloatField`) sufren errores de precisión binaria (ej. `0.1 + 0.2 = 0.30000000000000004`), inaceptables para transacciones financieras o presupuestos.

---

## 6. BATERÍA DE PREGUNTAS Y RESPUESTAS: DE LO MÁS SIMPLE A LO MÁS COMPLEJO

### BLOQUE A: FUNDAMENTOS BÁSICOS Y ENTORNO

#### P1: ¿Qué es Django y cuáles son sus ventajas principales?
**Respuesta:**  
Django es un framework web de alto nivel escrito en Python que fomenta el desarrollo rápido y el diseño limpio y pragmático. Sigue la filosofía *"Batteries Included"* (baterías incluidas), ofreciendo de serie autenticación de usuarios, panel de administración, protección de seguridad (CSRF, inyección SQL, XSS) y un sistema ORM robusto sin tener que instalar librerías externas para tareas básicas.

#### P2: ¿Qué arquitectura sigue Django? ¿Es MVC?
**Respuesta:**  
Django sigue el patrón **MVT (Model - View - Template)**, que es una variante del clásico MVC (Model - View - Controller):
- **Model (Modelo):** Define la estructura de datos y las reglas de negocio (capa de datos).
- **View (Vista):** Contiene la lógica de control. Recibe la petición HTTP, consulta los modelos y decide qué respuesta devolver. En el MVC tradicional equivaldría al *Controller*.
- **Template (Plantilla):** Es la capa de presentación (HTML con etiquetas de plantilla Django). En MVC equivaldría a la *View*.  
El framework Django actúa como el despachador central que une estos tres componentes.

#### P3: ¿Para qué sirve el archivo `manage.py`?
**Respuesta:**  
Es el script de administración local del proyecto. Permite interactuar con Django desde la terminal para arrancar el servidor de desarrollo (`runserver`), gestionar migraciones (`makemigrations`, `migrate`), crear superusuarios (`createsuperuser`), ejecutar pruebas o lanzar comandos personalizados como `python manage.py cargar_ejemplo`.

#### P4: ¿Cómo se arranca el proyecto en un equipo nuevo?
**Respuesta:**  
Basta con ejecutar el script `iniciar.bat` en Windows o `bash iniciar.sh` en Linux/Mac. El script crea el entorno virtual (`venv`), instala las dependencias de `requirements.txt`, ejecuta las migraciones pendientes, ejecuta `cargar_ejemplo` (creando el superusuario `admin` con clave `admin1234` y datos de prueba) y levanta el servidor en `http://127.0.0.1:8000/`.

---

### BLOQUE B: MODELOS, FORMULARIOS Y BASE DE DATOS

#### P5: ¿Qué diferencia existe entre `makemigrations` y `migrate`?
**Respuesta:**  
- `makemigrations`: Inspecciona los modelos en `models.py`, detecta las modificaciones realizadas y genera un archivo de migración en la carpeta `migrations/` con las instrucciones en código Python de los cambios que deben realizarse. No altera la base de datos física.
- `migrate`: Lee los archivos de migración pendientes y ejecuta las instrucciones SQL correspondientes en el motor de base de datos (SQLite en nuestro caso), creando o modificando las tablas y columnas reales.

#### P6: ¿Cuál es la diferencia entre `null=True` y `blank=True`?
**Respuesta:**  
- `null=True`: Es una restricción **a nivel de base de datos**. Permite que la columna admita valores `NULL`.
- `blank=True`: Es una validación **a nivel de formulario y aplicación**. Permite que el usuario deje el campo vacío al rellenar un formulario.  
*Ejemplo en el proyecto:* En `cierre_previsto` de Oportunidad se usan ambos (`null=True, blank=True`) porque un trabajo puede no tener fecha estimada de entrega y en la base de datos se guarda como `NULL`.

#### P7: ¿Qué relaciones entre modelos has utilizado y cómo funcionan las políticas de borrado (`on_delete`)?
**Respuesta:**  
Hemos utilizado relaciones muchos a uno mediante `ForeignKey`:
- `Oportunidad -> Contacto`: usa `on_delete=models.CASCADE`. Si se elimina un cliente, sus oportunidades de trabajo asociadas se eliminan en cascada.
- `Interaccion -> Contacto`: usa `models.CASCADE`.
- `Interaccion -> User (autor)`: usa `models.SET_NULL` (con `null=True`). Si se da de baja a un mecánico o empleado, no perdemos el histórico de las notas de la reparación; el campo `autor` pasa a estar vacío.
- `Recambio -> Contacto (proveedor)`: usa `models.SET_NULL`. Si se elimina un proveedor, las piezas en el almacén no se borran; simplemente quedan pendientes de asignar a otro proveedor.

#### P8: ¿Para qué sirve el parámetro `related_name` en una ForeignKey?
**Respuesta:**  
Permite definir el nombre de la relación inversa desde el modelo apuntado hacia el modelo de origen.  
*Ejemplo:* En `Oportunidad`, definimos `contacto = ForeignKey(Contacto, related_name='oportunidades')`. Gracias a esto, si tenemos una instancia de un contacto `c`, podemos obtener todos sus trabajos directamente en Python o en plantillas escribiendo `c.oportunidades.all()`, tal como se utiliza en `contactos/templates/contactos/detalle.html`.

#### P9: ¿Qué es un `ModelForm` y por qué es mejor que un formulario HTML convencional?
**Respuesta:**  
Un `ModelForm` es una clase que enlaza automáticamente un formulario con un modelo de Django.  
Ventajas:
1. Genera los campos HTML y tipos de entrada (`inputs`, `selects`, `textareas`) de forma automática a partir de los tipos de columna.
2. Aplica automáticamente las validaciones del modelo (longitud máxima, valores permitidos en `choices`, campos obligatorios).
3. Permite guardar directamente los datos en la base de datos invocando `form.save()`, evitando tener que extraer manualmente variable por variable desde `request.POST`.

---

### BLOQUE C: VISTAS, LÓGICA DE NEGOCIO Y SEGURIDAD

#### P10: ¿Qué es el middleware CSRF y por qué es obligatorio usar `{% csrf_token %}`?
**Respuesta:**  
CSRF (*Cross-Site Request Forgery* o Falsificación de Petición en Sitios Cruzados) es un ataque donde un sitio malicioso engaña al navegador de un usuario autenticado para que envíe una petición destructiva sin su consentimiento.  
Django genera un token criptográfico único por sesión. Al incluir `{% csrf_token %}` en los formularios POST, Django valida que la petición proviene realmente de nuestra aplicación y no de un sitio externo. Si falta el token o no coincide, devuelve un error HTTP 403 Forbidden.

#### P11: ¿Por qué protegiste las acciones de marcar como ganada o marcar tarea hecha con `@require_POST` en lugar de usar un enlace normal `<a>` con GET?
**Respuesta:**  
Según el estándar HTTP (RFC 7231), las peticiones **GET deben ser seguras e idempotentes**; es decir, solo deben consultar información, nunca provocar efectos secundarios ni mutar datos en el servidor.  
Si usáramos enlaces GET:
1. Un bot rastreador web (como el crawler de Google) podría seguir todos los enlaces de la página y marcar todas las tareas o presupuestos como ganados sin intervención humana.
2. El navegador podría pre-cargar enlaces en segundo plano para acelerar la navegación, ejecutando la acción sin que el usuario haya hecho clic.
3. Sería vulnerable a ataques de inyección de imagen o enlaces CSRF (`<img src="/tareas/1/hecha/">`).  
Con `@require_POST`, solo se aceptan envíos deliberados mediante formularios protegidos con token.

#### P12: ¿Cómo funciona el decorador `@login_required`?
**Respuesta:**  
Verifica si el usuario actual está autenticado (`request.user.is_authenticated`). Si no lo está, intercepta la petición y redirige al usuario a la URL configurada en `settings.LOGIN_URL` (`/login/`), añadiendo el parámetro `?next=/ruta/original` para que, tras iniciar sesión correctamente, el usuario regrese a la pantalla donde intentaba acceder.

#### P13: ¿Cómo funciona la búsqueda con filtros múltiples usando `Q` objects?
**Respuesta:**  
Por defecto, al pasar varios argumentos a `.filter()`, Django los une con el operador lógico `AND`. Para realizar búsquedas con operador `OR` (por ejemplo, buscar por nombre **o** por matrícula **o** por vehículo), Django proporciona la clase `Q`.  
En `contactos/views.py`:
```python
objetos.filter(Q(nombre__icontains=q) | Q(matricula__icontains=q) | Q(vehiculo__icontains=q))
```
Esto genera una cláusula SQL: `WHERE (nombre LIKE '%q%' OR matricula LIKE '%q%' OR vehiculo LIKE '%q%')`. El modificador `__icontains` asegura que la búsqueda sea insensible a mayúsculas y acentos.

---

### BLOQUE D: CONSULTAS AVANZADAS ORM Y AGREGACIONES

#### P14: Explica en detalle cómo calculas la tabla de "Importe total por etapa" en Oportunidades.
**Respuesta:**  
Se utiliza la combinación de `.values()` y `.annotate()` del ORM de Django:
```python
agrupado = {
    fila['etapa']: fila
    for fila in Oportunidad.objects.values('etapa').annotate(total=Sum('importe'), n=Count('id'))
}
```
1. `.values('etapa')`: Equivale a la cláusula SQL `GROUP BY etapa`. Agrupa todas las filas de la tabla por su valor de etapa.
2. `.annotate(total=Sum('importe'), n=Count('id'))`: Calcula para cada grupo la suma de la columna importe y el recuento de oportunidades (`SELECT etapa, SUM(importe) AS total, COUNT(id) AS n FROM oportunidades GROUP BY etapa`).
3. Construcción del diccionario y lista: En Python convertimos el resultado en un diccionario indexado por etapa y recorremos las etapas oficiales definidas en `Oportunidad.ETAPAS`. Así garantizamos que, incluso si una etapa no tiene ningún trabajo registrado, se muestre en la tabla con `0 trabajos` y `0 €`.

#### P15: ¿Qué es una expresión `F()` y por qué la utilizas en la métrica de recambios?
**Respuesta:**  
En Django ORM, la clase `F()` representa el valor de una columna directamente en la consulta SQL, sin necesidad de transferir el dato a Python.  
Normalmente se compara una columna con una constante (`stock__lte=5`). Sin embargo, en nuestro almacén cada recambio tiene un umbral de seguridad diferente (`stock_minimo`).  
Para detectar qué piezas están por debajo de su propio mínimo, escribimos:
```python
Recambio.objects.filter(stock__lte=F('stock_minimo'))
```
Esto produce en SQL: `WHERE stock <= stock_minimo`. La comparación se ejecuta dentro del motor de base de datos de manera atómica y eficiente.

#### P16: ¿Qué es el problema de las consultas N+1 y cómo lo solucionas?
**Respuesta:**  
Ocurre cuando listamos `N` registros de un modelo que tiene una clave foránea (por ejemplo, 50 oportunidades y sus respectivos clientes) y en la plantilla accedemos al cliente de cada uno (`{{ o.contacto.nombre }}`).  
Sin optimización, Django ejecuta 1 consulta para traer las 50 oportunidades, y luego **50 consultas adicionales** (una por fila) para consultar el contacto de cada oportunidad (total = 51 consultas).  
Lo solucionamos en la vista con `select_related('contacto')`:
```python
objetos = Oportunidad.objects.select_related('contacto')
```
`select_related` realiza un `INNER JOIN` en SQL, trayendo todos los datos del contacto en la misma y única consulta inicial.

---

### BLOQUE E: ARQUITECTURA, ESCALABILIDAD Y NIVEL EXPERTO

#### P17: ¿Cómo funciona el sistema de módulos dinámicos (`MODULOS_CRM`)?
**Respuesta:**  
En `settings.py` definimos la lista `MODULOS_CRM`. Esta variable se aprovecha en tres puntos clave:
1. En `INSTALLED_APPS`: Se concatenan automáticamente los módulos (`INSTALLED_APPS = [...] + MODULOS_CRM`).
2. En `crm_project/urls.py`: Se registran sus rutas automáticamente mediante un bucle (`for modulo in settings.MODULOS_CRM: urlpatterns.append(...)`).
3. En `core/context_processors.py`: Se inyecta en el contexto global de las plantillas una lista de enlaces para pintar la barra de navegación dinámicamente.  
Además, en `core/views.py`, la función auxiliar `_modelo(app, nombre)` utiliza `apps.get_model()` con captura de `LookupError`. Si se desactiva un módulo de la lista, el Dashboard no se rompe ni lanza una excepción; simplemente oculta la tarjeta y métricas correspondientes.

#### P18: En `interacciones`, ¿por qué no se incluye el campo `autor` en el formulario?
**Respuesta:**  
Por dos motivos fundamentales:
1. **Seguridad:** Si el campo `autor` estuviera en el formulario (por ejemplo con `fields='__all__'`), un usuario podría interceptar la petición POST y alterar el ID del autor para falsear quién registró una llamada o una visita en el mostrador.
2. **Experiencia de usuario (UX):** No tiene sentido obligar a un usuario a seleccionarse a sí mismo en un desplegable cuando el sistema ya sabe quién ha iniciado sesión mediante `request.user`.  
Por ello, excluimos el campo del formulario y en la vista usamos:
```python
obj = form.save(commit=False)
obj.autor = request.user
obj.save()
```

#### P19: ¿Cómo pasarías este proyecto a un entorno de producción real?
**Respuesta:**  
Para un despliegue en producción profesional, realizaría las siguientes configuraciones:
1. **Seguridad en `settings.py`:**
   - Cambiar `DEBUG = False`.
   - Cargar `SECRET_KEY` y credenciales sensibles desde variables de entorno (`.env` o gestor de secretos).
   - Configurar `ALLOWED_HOSTS = ['taller.midominio.com']`.
   - Activar cookies seguras: `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True`, y cabeceras HSTS.
2. **Base de Datos:** Migrar de SQLite3 a un motor cliente-servidor concurrente como **PostgreSQL**, actualizando `DATABASES['default']['ENGINE']`.
3. **Servidor de Aplicaciones y Web:**
   - Usar un servidor WSGI como **Gunicorn** o **uWSGI** para ejecutar los procesos Python.
   - Poner un proxy inverso con **Nginx** por delante para gestionar conexiones HTTPS/SSL, balanceo de carga y compresión Gzip.
4. **Archivos Estáticos:**
   - Configurar `STATIC_ROOT` y ejecutar `python manage.py collectstatic`.
   - Servirlos con Nginx o mediante librerías como **WhiteNoise** o un CDN (AWS S3 / Cloudflare).

---

## 7. GUIÓN DE DEMOSTRACIÓN EN VIVO (PASO A PASO EN 3 MINUTOS)

Si el tribunal te pide: *"Pruébalo y enséñanos lo que has hecho"*, sigue exactamente este orden para no titubear:

```
[1. DASHBOARD]  ──► [2. CONTACTOS] ──► [3. OPORTUNIDADES] ──► [4. TAREAS] ──► [5. RECAMBIOS]
```

### Paso 1: Dashboard Inicial (`/`)
- Muestra el encabezado con el nombre `AutoTaller CRM` y el color corporativo naranja (`#d35400`).
- Señala las tarjetas de resumen: los 5 módulos activos.
- Enseña las métricas en tiempo real:
  - Destaca la métrica **Tareas vencidas** (aparece en rojo `#c0392b`).
  - Destaca los **Coches en reparación ahora**.
  - Destaca la métrica de **Recambios con stock bajo** (alerta en rojo).

### Paso 2: Módulo de Contactos (`/contactos/`)
- Muestra las columnas añadidas: **Matrícula** y **Vehículo**.
- Haz una prueba de búsqueda: escribe una matrícula (ej. `4821 KLM` o `FRT`) o una marca (ej. `Seat` o `Golf`). Demuestra cómo filtra por múltiples campos.
- Utiliza el desplegable para filtrar por tipo (ej. `Cliente particular` o `Proveedor de recambios`).
- Entra en la ficha de un contacto (ej. *Carlos Martín Ruiz*): enseña cómo la ficha muestra los datos del coche y, gracias al `related_name`, carga su historial de intervenciones, trabajos abiertos y tareas.

### Paso 3: Módulo de Oportunidades / Trabajos (`/oportunidades/`)
- Muestra la tabla principal con las etapas del taller (`Presupuesto`, `Aprobado`, `En reparación`...).
- Filtra por etapa: selecciona `En reparación` para ver los coches actualmente en el taller.
- Desplázate al pie de la página y **muestra la funcionalidad del Nivel 3**: la tabla de **"Importe total por etapa"**, explicando que utiliza agregaciones SQL con `values('etapa').annotate(Sum('importe'))`.
- Entra en una oportunidad que esté en presupuesto o aprobada: pulsa el botón **"✔ Marcar como ganada (vehículo entregado)"**. Muestra cómo cambia de estado mediante POST y cómo ahora aparece el banner verde indicando que el vehículo ha sido entregado.
- Vuelve al Dashboard: muestra cómo la facturación total ganada se ha incrementado automáticamente.

### Paso 4: Módulo de Tareas (`/tareas/`)
- Enseña la columna **Prioridad** (`Alta`, `Media`, `Baja`) y cómo las tareas vencidas aparecen marcadas en rojo con la etiqueta *(vencida)*.
- **Muestra la segunda funcionalidad del Nivel 3**: pulsa el botón **"✔ Hecha"** en una de las tareas pendientes. Señala que con un solo clic (vía POST) la tarea pasa a estado completada y desaparece el botón.

### Paso 5: Módulo de Recambios (Nivel 4 - Almacén) (`/recambios/`)
- Explica que es una app creada desde cero con `startapp` para dotar de valor real al taller.
- Muestra cómo los artículos que tienen `stock <= stock_minimo` muestran el indicador **"⚠ reponer"** en rojo gracias a la propiedad `@property stock_bajo`.
- Demuestra que al dar de alta un recambio (`+ Nuevo`), el desplegable de proveedores solo muestra contactos que sean de tipo `proveedor`, gracias al parámetro `limit_choices_to={'tipo': 'proveedor'}`.

---

## 8. CHULETA DE COMANDOS RÁPIDOS POR SI TE PIDEN PROBAR EN VIVO

Ten esta tabla a mano por si te piden abrir una terminal durante la defensa:

| Acción solicitada | Comando a ejecutar en la terminal |
|---|---|
| **Reiniciar la base de datos desde cero** | Borrar el archivo `db.sqlite3` y ejecutar `python manage.py migrate` seguido de `python manage.py cargar_ejemplo`. |
| **Crear un nuevo superusuario** | `python manage.py createsuperuser` |
| **Abrir la consola interactiva de Django** | `python manage.py shell` |
| **Consultar facturación en consola** | `from oportunidades.models import *; from django.db.models import Sum; Oportunidad.objects.filter(etapa='entregado').aggregate(Sum('importe'))` |
| **Comprobar si hay errores en el proyecto** | `python manage.py check` |
| **Listar las migraciones aplicadas** | `python manage.py showmigrations` |

---

> 💡 **Consejo final para la exposición:**  
> Habla con calma, mira a los evaluadores y mantén la iniciativa. Cuando expliques una pantalla, no te limites a decir "aquí hay un botón"; explica **qué hace por detrás** (ej: *"este botón envía un POST con token CSRF a la vista `marcar_ganada`, que actualiza el estado a `entregado` y realiza una redirección segura"*). Eso demuestra solvencia y dominio completo del código. ¡Mucho éxito en la defensa!
