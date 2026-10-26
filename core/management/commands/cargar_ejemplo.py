"""
Comando:  python manage.py cargar_ejemplo
Crea el usuario admin (clave admin1234) y datos de ejemplo para que el CRM no esté vacío.
Es seguro ejecutarlo varias veces: no duplica datos.
TODO 10 (hecho): datos de ejemplo de un TALLER MECÁNICO (10 contactos, trabajos, avisos, tareas y recambios).
Los nombres, teléfonos, emails y matrículas son inventados.
"""
from datetime import date, timedelta
from django.apps import apps
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Carga usuario admin y datos de ejemplo'

    def handle(self, *args, **opciones):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
            self.stdout.write('Usuario creado: admin / admin1234')
        try:
            Contacto = apps.get_model('contactos', 'Contacto')
        except LookupError:
            return
        if Contacto.objects.exists():
            self.stdout.write('Ya había datos; no se carga nada más.')
            return

        hoy = date.today()   # Las fechas se calculan respecto a hoy para que los datos nunca "caduquen"

        # ---------------- CONTACTOS (10): clientes particulares, empresas, proveedores y aseguradora ----------------
        c1 = Contacto.objects.create(nombre='Carlos Martín Ruiz', tipo='particular', matricula='4821 KLM', vehiculo='Seat León 1.6 TDI',
                                     email='carlos.martin@example.com', telefono='600100201', notas='Cliente desde 2021. Prefiere que le avisen por WhatsApp.')
        c2 = Contacto.objects.create(nombre='Lucía Fernández Gil', tipo='particular', matricula='7350 HGT', vehiculo='Renault Clio 0.9 TCe',
                                     email='lucia.fernandez@example.com', telefono='600100202', notas='Pasa la ITV en pocas semanas.')
        c3 = Contacto.objects.create(nombre='Transportes Hermanos Vega SL', tipo='empresa', matricula='2294 MVD', vehiculo='Ford Transit 2.0 TDCi (furgoneta de reparto)',
                                     email='flota@hermanosvega.example', telefono='910100203', notas='Flota de 3 furgonetas. Factura mensual.')
        c4 = Contacto.objects.create(nombre='Javier Ortega Soto', tipo='particular', matricula='9013 FRT', vehiculo='Volkswagen Golf VII 2.0 TDI',
                                     email='javier.ortega@example.com', telefono='600100204')
        c5 = Contacto.objects.create(nombre='Marta Domínguez Pardo', tipo='particular', matricula='5567 BNZ', vehiculo='Toyota Yaris Hybrid',
                                     email='marta.dominguez@example.com', telefono='600100205', notas='Vehículo híbrido: revisar batería en cada mantenimiento.')
        c6 = Contacto.objects.create(nombre='Recambios Hidalgo SA', tipo='proveedor',
                                     email='pedidos@recambioshidalgo.example', telefono='910100206', notas='Reparto en 24 h. Pedido mínimo 50 €.')
        c7 = Contacto.objects.create(nombre='Neumáticos Rápidos SL', tipo='proveedor',
                                     email='ventas@neumaticosrapidos.example', telefono='910100207', notas='Mejor precio en neumáticos de 16" y 17".')
        c8 = Contacto.objects.create(nombre='Seguros Iberia Mutua', tipo='aseguradora',
                                     email='peritaciones@segurosiberia.example', telefono='910100208', notas='Convenio de reparaciones concertadas.')
        c9 = Contacto.objects.create(nombre='Distribuciones Norte SL', tipo='empresa', matricula='3178 CWP', vehiculo='Citroën Berlingo BlueHDi',
                                     email='administracion@distribucionesnorte.example', telefono='910100209')
        c10 = Contacto.objects.create(nombre='Pablo Navarro León', tipo='particular', matricula='6642 DKS', vehiculo='BMW 320d (2014)',
                                      email='pablo.navarro@example.com', telefono='600100210')

        # ---------------- OPORTUNIDADES = trabajos del taller (una o varias por etapa) ----------------
        try:
            Op = apps.get_model('oportunidades', 'Oportunidad')
            Op.objects.create(titulo='Cambio de embrague completo', contacto=c1, etapa='en_reparacion', importe=780, cierre_previsto=hoy + timedelta(days=2))
            Op.objects.create(titulo='Revisión pre-ITV y cambio de aceite', contacto=c2, etapa='presupuesto', importe=145.50, cierre_previsto=hoy + timedelta(days=10))
            Op.objects.create(titulo='Mantenimiento anual de la flota (3 furgonetas)', contacto=c3, etapa='aprobado', importe=2400, cierre_previsto=hoy + timedelta(days=15))
            Op.objects.create(titulo='Cambio de pastillas y discos delanteros', contacto=c4, etapa='entregado', importe=320)
            Op.objects.create(titulo='Sustitución de correa de distribución', contacto=c5, etapa='presupuesto', importe=590, cierre_previsto=hoy + timedelta(days=20))
            Op.objects.create(titulo='Convenio de reparaciones concertadas', contacto=c8, etapa='aprobado', importe=6000, cierre_previsto=hoy + timedelta(days=30))
            Op.objects.create(titulo='Diagnosis electrónica por testigo de motor', contacto=c10, etapa='rechazado', importe=90)
            Op.objects.create(titulo='Cambio de 4 neumáticos y alineado', contacto=c9, etapa='entregado', importe=410)
            Op.objects.create(titulo='Cambio de aceite y filtros', contacto=c9, etapa='en_reparacion', importe=120, cierre_previsto=hoy + timedelta(days=1))
        except LookupError:
            pass

        # ---------------- INTERACCIONES (con los canales nuevos: WhatsApp y En mostrador) ----------------
        try:
            Inter = apps.get_model('interacciones', 'Interaccion')
            admin = User.objects.get(username='admin')
            Inter.objects.create(contacto=c1, canal='llamada', resumen='Avería: el embrague patina en cuesta. Se acuerda traer el coche el lunes.', autor=admin)
            Inter.objects.create(contacto=c1, canal='whatsapp', resumen='Enviado el presupuesto del embrague en PDF. Lo acepta.', autor=admin)
            Inter.objects.create(contacto=c2, canal='mostrador', resumen='Viene a pedir presupuesto de revisión antes de la ITV.', autor=admin)
            Inter.objects.create(contacto=c3, canal='reunion', resumen='Reunión para cerrar el plan de mantenimiento anual de las furgonetas.', autor=admin)
            Inter.objects.create(contacto=c4, canal='whatsapp', resumen='Aviso: el coche ya está listo para recoger.', autor=admin)
            Inter.objects.create(contacto=c6, canal='email', resumen='Pedido de pastillas de freno y filtros de aceite.', autor=admin)
            Inter.objects.create(contacto=c8, canal='email', resumen='Enviadas las tarifas de mano de obra para el convenio.', autor=admin)
            Inter.objects.create(contacto=c10, canal='nota', resumen='Rechaza el presupuesto de diagnosis; lo llevará a otro taller.', autor=admin)
        except LookupError:
            pass

        # ---------------- TAREAS (con prioridad; alguna ya vencida para que se vea la métrica) ----------------
        try:
            Tarea = apps.get_model('tareas', 'Tarea')
            Tarea.objects.create(titulo='Avisar a Carlos: el coche estará listo', contacto=c1, prioridad='alta', vence=hoy + timedelta(days=2))
            Tarea.objects.create(titulo='Recordar a Lucía la fecha de su ITV', contacto=c2, prioridad='media', vence=hoy + timedelta(days=5))
            Tarea.objects.create(titulo='Enviar factura mensual a Transportes Vega', contacto=c3, prioridad='alta', vence=hoy - timedelta(days=2))
            Tarea.objects.create(titulo='Pedir pastillas de freno a Recambios Hidalgo', contacto=c6, prioridad='alta', vence=hoy - timedelta(days=1))
            Tarea.objects.create(titulo='Llamar a Marta para confirmar el presupuesto de la correa', contacto=c5, prioridad='media', vence=hoy + timedelta(days=3))
            Tarea.objects.create(titulo='Revisar tarifas de neumáticos del proveedor', contacto=c7, prioridad='baja', vence=hoy + timedelta(days=14))
            Tarea.objects.create(titulo='Cobrar el cambio de pastillas a Javier', contacto=c4, prioridad='media', vence=hoy - timedelta(days=4), hecha=True)
            Tarea.objects.create(titulo='Limpiar y ordenar el almacén de recambios', prioridad='baja', vence=hoy + timedelta(days=7))
        except LookupError:
            pass

        # ---------------- RECAMBIOS (módulo propio): algunos con stock bajo ----------------
        try:
            Recambio = apps.get_model('recambios', 'Recambio')
            Recambio.objects.create(referencia='FR-PD-0112', nombre='Pastillas de freno delanteras', categoria='frenos', proveedor=c6, precio=38.90, stock=1, stock_minimo=4)
            Recambio.objects.create(referencia='FR-DS-0210', nombre='Disco de freno delantero (par)', categoria='frenos', proveedor=c6, precio=84.00, stock=3, stock_minimo=2)
            Recambio.objects.create(referencia='FL-AC-0305', nombre='Filtro de aceite', categoria='filtros', proveedor=c6, precio=7.50, stock=12, stock_minimo=6)
            Recambio.objects.create(referencia='FL-AI-0306', nombre='Filtro de aire', categoria='filtros', proveedor=c6, precio=11.20, stock=2, stock_minimo=5)
            Recambio.objects.create(referencia='AC-5W30-5L', nombre='Aceite sintético 5W30 (5 L)', categoria='filtros', proveedor=c6, precio=42.00, stock=8, stock_minimo=3)
            Recambio.objects.create(referencia='NE-2055R16', nombre='Neumático 205/55 R16', categoria='neumaticos', proveedor=c7, precio=68.00, stock=9, stock_minimo=4)
            Recambio.objects.create(referencia='EL-BAT-70AH', nombre='Batería 12V 70Ah', categoria='electrico', proveedor=c6, precio=96.50, stock=2, stock_minimo=2)
            Recambio.objects.create(referencia='MO-CORR-0415', nombre='Kit de distribución con bomba de agua', categoria='motor', precio=189.00, stock=0, stock_minimo=1)
        except LookupError:
            pass
        self.stdout.write('Datos de ejemplo cargados.')
