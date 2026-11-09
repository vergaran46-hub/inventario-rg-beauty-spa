-- ============================================================================
-- Referencia del esquema relacional del módulo (generado con
-- "python manage.py sqlmigrate inventario 0001/0002"). Es solo documentación:
-- las tablas se crean con "python manage.py migrate", que también crea
-- auth_user, de la que dependen las claves foráneas de usuario_id.
-- ============================================================================
--
-- Create model Categoria
--
CREATE TABLE `inventario_categoria` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(50) NOT NULL);
--
-- Create model Producto
--
CREATE TABLE `inventario_producto` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(100) NOT NULL, `descripcion` longtext NOT NULL, `stock_actual` integer UNSIGNED NOT NULL CHECK (`stock_actual` >= 0), `stock_minimo` integer UNSIGNED NOT NULL CHECK (`stock_minimo` >= 0), `categoria_id` bigint NULL);
--
-- Create model Movimiento
--
CREATE TABLE `inventario_movimiento` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `tipo` varchar(10) NOT NULL, `motivo` varchar(15) NOT NULL, `cantidad` integer UNSIGNED NOT NULL CHECK (`cantidad` >= 0), `fecha` datetime(6) NOT NULL, `usuario_id` integer NULL, `producto_id` bigint NOT NULL);
ALTER TABLE `inventario_producto` ADD CONSTRAINT `inventario_producto_categoria_id_7033fb47_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`);
ALTER TABLE `inventario_movimiento` ADD CONSTRAINT `inventario_movimiento_usuario_id_f452f794_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `inventario_movimiento` ADD CONSTRAINT `inventario_movimient_producto_id_4356cb23_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`);
--
-- Create model Etiqueta
--
CREATE TABLE `inventario_etiqueta` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(40) NOT NULL);
--
-- Add field usuario to producto
--
ALTER TABLE `inventario_producto` ADD COLUMN `usuario_id` integer NULL , ADD CONSTRAINT `inventario_producto_usuario_id_1e985dad_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user`(`id`);
--
-- Add field etiquetas to producto
--
CREATE TABLE `inventario_producto_etiquetas` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `producto_id` bigint NOT NULL, `etiqueta_id` bigint NOT NULL);
ALTER TABLE `inventario_producto_etiquetas` ADD CONSTRAINT `inventario_producto_etiq_producto_id_etiqueta_id_2738a27e_uniq` UNIQUE (`producto_id`, `etiqueta_id`);
ALTER TABLE `inventario_producto_etiquetas` ADD CONSTRAINT `inventario_producto__producto_id_2275f603_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`);
ALTER TABLE `inventario_producto_etiquetas` ADD CONSTRAINT `inventario_producto__etiqueta_id_d69a4543_fk_inventari` FOREIGN KEY (`etiqueta_id`) REFERENCES `inventario_etiqueta` (`id`);
