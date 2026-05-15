# ReservaTech - Gestor de Reservas

Este es un sistema completo de gestión de reservas desarrollado con Django. Permite a los usuarios consultar espacios (pistas deportivas, salas de reuniones, etc.) y realizar reservas visualizándolas en un calendario interactivo.

## Características Principales
- **Catálogo de Espacios:** Visualización de todos los recursos disponibles para reservar.
- **Calendario Interactivo:** Integración con FullCalendar para ver las reservas en tiempo real.
- **Gestión de Disponibilidad:** Sistema de reglas de horario (días y horas de apertura) para cada espacio.
- **Panel de Administración Premium:** Interfaz de administración moderna usando Django Jazzmin para gestionar usuarios, reservas e instalaciones.
- **Diseño Moderno:** Interfaz de usuario (UI) adaptativa, con un modo oscuro estilizado con acentos de neón púrpura y rosa.

## Acceso de Evaluación 

El proyecto se encuentra desplegado y listo para su uso en producción. Puedes probar el panel de administración utilizando las siguientes credenciales:

**URL Pública:** https://gestor-de-reservas-ne0x.onrender.com

### Panel de Administración
Para entrar al panel de control y gestionar todo el sistema (crear espacios, ver todos los usuarios, etc.):
1. Ve a la URL pública y añade `/admin` al final.
2. Utiliza las siguientes credenciales de superusuario:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

## Tecnologías Utilizadas
- **Backend:** Python, Django 6.0
- **Base de Datos:** PostgreSQL (Producción) / SQLite (Desarrollo local)
- **Frontend:** HTML5, Vanilla CSS, JavaScript, FullCalendar, Bootstrap
- **Despliegue:** Render.com, Gunicorn, WhiteNoise (Gestión de archivos estáticos)