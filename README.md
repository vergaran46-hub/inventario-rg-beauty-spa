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
2. Crear la base de datos y el usuario de la aplicación.
   - Guarda una copia de `database/crear_base_de_datos.sql` fuera del repositorio con el nombre `crear_base_local.sql`. Reemplaza `CAMBIAR_ESTA_CLAVE` por tu contraseña de MySQL para `inventario_app` en esa copia.
   - Abre una terminal en la carpeta donde guardaste la copia. Ejecuta este comando y escribe la contraseña de `root` de MySQL cuando se solicite.

     ```sh
     mysql -u root -p -e "source crear_base_local.sql"
     ```

     Si PowerShell no encuentra `mysql`, usa `& 'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe'` en su lugar y ajusta la ruta a tu instalación.
   - El script crea la base `inventario_rg_beauty` y otorga a `inventario_app` permisos sobre ella. Django crea las tablas mediante las migraciones del paso 4.
   - Comprueba la base y el acceso con la contraseña de `inventario_app`. El resultado debe mostrar `inventario_rg_beauty`.

     ```sh
     mysql -u inventario_app -p -D inventario_rg_beauty -e "SELECT DATABASE();"
     ```

3. Vuelve a la carpeta del repositorio y define `DB_PASSWORD` con la contraseña de `inventario_app` en la misma terminal donde ejecutarás Django. Consulta `.env.example` para ver las demás variables disponibles.
   - En Windows (PowerShell), puedes ingresarla de forma oculta.

     ```powershell
     $env:DB_PASSWORD = [System.Net.NetworkCredential]::new('', (Read-Host 'Clave MySQL de inventario_app' -AsSecureString)).Password
     ```

   - En Linux/macOS (Bash o Zsh), ejecuta lo siguiente e ingresa la contraseña cuando la terminal espere tu entrada.

     ```sh
     read -rs DB_PASSWORD
     export DB_PASSWORD
     ```

4. Crear las tablas y un administrador, y ejecutar:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Abrir http://127.0.0.1:8000/

## Cuentas y roles

- El registro público está activado por defecto. Para desactivarlo, define `DJANGO_REGISTRO_ABIERTO=False`.
- Crea una cuenta administradora con `python manage.py createsuperuser`.
- Desde el inventario, cada usuaria solo puede editar o eliminar sus propios productos.
- Tras 5 intentos fallidos, el inicio de sesión se bloquea durante 15 minutos para esa combinación de usuario y dirección IP.

## Pruebas automatizadas
```
python manage.py test
```
Django crea y elimina la base temporal al ejecutar la suite.

## Solución de problemas comunes

- **`Access denied for user 'inventario_app'@'localhost'` (`1045`).** Comprueba que `DB_PASSWORD` esté definida en la terminal donde ejecutas Django y coincida con la contraseña de la cuenta. Si el usuario ya existía, el script conserva su contraseña anterior.
- **Error `1044` al crear `test_inventario_rg_beauty`.** Una cuenta administradora de MySQL debe otorgar a `inventario_app`, sobre esa base de pruebas, los mismos permisos que el script otorga sobre `inventario_rg_beauty`.
- **`ModuleNotFoundError` al ejecutar Django.** Activa el entorno virtual y ejecuta `pip install -r requirements.txt` como se indica en [Puesta en marcha](#puesta-en-marcha).

## Estructura
- `config/`: configuración del proyecto (settings, urls).
- `inventario/`: aplicación (models, forms, views, templates, tests, migrations).
- `database/`: script de creación de la base y referencia del esquema.

## Producción
Definir `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS`; con eso se activan HTTPS obligatorio,
cookies seguras y HSTS.
