# Inventario RG Beauty Spa (prototipo)

Módulo de gestión de inventario y stock para RG Beauty Spa. Desarrollado con Django 5.1 y MySQL.
Proyecto de la asignatura Ingeniería de Software (INACAP, Copiapó).

## Funcionalidades
- Registro de usuarios, inicio y cierre de sesión, cambio de contraseña y perfil.
- Alta, consulta, edición y eliminación de productos con grupos y etiquetas.
- Registro de entradas y salidas de stock con historial y validación de existencias.
- Pantalla de inicio con los productos que alcanzaron su stock mínimo.
- Buscador, filtro por grupo y paginación del listado.

## Requisitos
- Python 3.11 o superior
- MySQL 8.x o MariaDB 10.6 o superior

## Puesta en marcha
1. Crear el entorno e instalar dependencias:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)   |   source venv/bin/activate   (Linux/macOS)
   pip install -r requirements.txt
   ```
2. Crear la base de datos y el usuario (editar antes la clave en el script):
   ```
   mysql -u root -p < database/crear_base_de_datos.sql
   ```
3. Definir las variables de entorno (ver `.env.example`). Mínimo `DB_PASSWORD`.
   - Windows (PowerShell): `$env:DB_PASSWORD="su-clave"`
   - Linux/macOS: `export DB_PASSWORD=su-clave`
4. Crear las tablas y un administrador, y ejecutar:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Abrir http://127.0.0.1:8000/

## Pruebas automatizadas
```
python manage.py test
```
(el usuario de la base necesita permiso para crear `test_inventario_rg_beauty`).

## Estructura
- `config/`: configuración del proyecto (settings, urls).
- `inventario/`: aplicación (models, forms, views, templates, tests, migrations).
- `database/`: script de creación de la base y referencia del esquema.

## Producción
Definir `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS`; con eso se activan HTTPS obligatorio,
cookies seguras y HSTS.
