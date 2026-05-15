import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@reservatech.com', 'admin123')
        print("✅ Superusuario 'admin' creado exitosamente.")
    else:
        # Forzar el cambio de contraseña por si acaso
        u = User.objects.get(username='admin')
        u.set_password('admin123')
        u.save()
        print("✅ Superusuario 'admin' ya existía. Contraseña restablecida a admin123.")
except Exception as e:
    print(f"❌ Error al crear el superusuario: {e}")
