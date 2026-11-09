-- ============================================================================
-- Script de creación de la base de datos - Inventario RG Beauty Spa
-- Motor: MySQL 8.x / MariaDB 10.6+
-- Uso:   mysql -u root -p < database/crear_base_de_datos.sql
-- Este script crea la base de datos y el usuario de la aplicación, con
-- privilegios solo sobre esa base. Las tablas se crean después con las
-- migraciones de Django (python manage.py migrate), que incluyen las tablas
-- de autenticación y sesiones. Cambie la contraseña antes de usarlo y
-- repítala en la variable de entorno DB_PASSWORD.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS inventario_rg_beauty
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'inventario_app'@'localhost' IDENTIFIED BY 'CAMBIAR_ESTA_CLAVE';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES, DROP
    ON inventario_rg_beauty.* TO 'inventario_app'@'localhost';
FLUSH PRIVILEGES;
