from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Movimiento, Producto


class BaseTest(TestCase):
    def setUp(self):
        cache.clear()
        self.ana = User.objects.create_user('ana', 'ana@example.com', 'ClaveSegura#2026')
        self.beto = User.objects.create_user('beto', 'beto@example.com', 'ClaveSegura#2026')
        self.categoria = Categoria.objects.create(nombre='Facial')
        self.producto = Producto.objects.create(
            nombre='Crema hidratante', categoria=self.categoria,
            stock_actual=10, stock_minimo=3, usuario=self.ana,
        )

    def entrar(self, usuario='ana'):
        self.client.login(username=usuario, password='ClaveSegura#2026')


class AutenticacionTests(BaseTest):
    def test_rutas_protegidas_redirigen_al_login(self):
        for nombre, args in [('inicio', []), ('home', []), ('movimiento_crear', []),
                             ('producto_crear', []), ('producto_editar', [self.producto.pk]),
                             ('producto_eliminar', [self.producto.pk]), ('perfil', [])]:
            r = self.client.get(reverse(nombre, args=args))
            self.assertEqual(r.status_code, 302, nombre)
            self.assertIn(reverse('login'), r.url, nombre)

    def test_login_correcto_e_incorrecto(self):
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'mala'})
        self.assertEqual(r.status_code, 200)
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'ClaveSegura#2026'})
        self.assertEqual(r.status_code, 302)

    def test_bloqueo_tras_cinco_intentos_fallidos(self):
        for _ in range(5):
            self.client.post(reverse('login'), {'username': 'ana', 'password': 'mala'})
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'ClaveSegura#2026'})
        self.assertEqual(r.status_code, 429)

    def test_contrasena_se_guarda_cifrada(self):
        self.assertTrue(self.ana.password.startswith('pbkdf2_'))
        self.assertNotIn('ClaveSegura', self.ana.password)

    def test_registro_rechaza_contrasena_debil(self):
        r = self.client.post(reverse('registro'), {
            'username': 'nuevo', 'email': 'n@example.com',
            'password1': '12345678', 'password2': '12345678'})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username='nuevo').exists())

    def test_registro_valido(self):
        r = self.client.post(reverse('registro'), {
            'username': 'nuevo', 'email': 'n@example.com',
            'password1': 'OtraClave#Larga9', 'password2': 'OtraClave#Larga9'})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevo').exists())


class RegistroDeshabilitadoTests(BaseTest):
    def test_registro_cerrado_responde_404(self):
        from django.test import override_settings
        with override_settings(REGISTRO_ABIERTO=False):
            self.assertEqual(self.client.get(reverse('registro')).status_code, 404)
            r = self.client.post(reverse('registro'), {
                'username': 'intruso', 'email': 'i@example.com',
                'password1': 'OtraClave#Larga9', 'password2': 'OtraClave#Larga9'})
            self.assertEqual(r.status_code, 404)
        self.assertFalse(User.objects.filter(username='intruso').exists())


class AutorizacionTests(BaseTest):
    def test_otro_usuario_no_puede_editar_ni_eliminar(self):
        self.entrar('beto')
        self.assertEqual(self.client.get(reverse('producto_editar', args=[self.producto.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse('producto_eliminar', args=[self.producto.pk])).status_code, 403)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_duenio_puede_editar(self):
        self.entrar('ana')
        r = self.client.post(reverse('producto_editar', args=[self.producto.pk]), {
            'nombre': 'Crema facial', 'categoria': self.categoria.pk,
            'descripcion': '', 'stock_actual': 8, 'stock_minimo': 2})
        self.assertEqual(r.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Crema facial')

    def test_eliminar_requiere_post(self):
        self.entrar('ana')
        self.client.get(reverse('producto_eliminar', args=[self.producto.pk]))
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())


class ValidacionProductoTests(BaseTest):
    def crear(self, **datos):
        base = {'nombre': 'Mascarilla', 'descripcion': '', 'stock_actual': 5, 'stock_minimo': 1}
        base.update(datos)
        self.entrar()
        return self.client.post(reverse('producto_crear'), base)

    def test_producto_valido(self):
        self.assertEqual(self.crear().status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre='Mascarilla', usuario=self.ana).exists())

    def test_nombre_corto_o_solo_numeros(self):
        for nombre in ['ab', '12345']:
            self.assertEqual(self.crear(nombre=nombre).status_code, 200)
        self.assertFalse(Producto.objects.filter(nombre__in=['ab', '12345']).exists())

    def test_stock_fuera_de_rango(self):
        self.assertEqual(self.crear(stock_actual=101).status_code, 200)
        self.assertEqual(self.crear(stock_actual=-1).status_code, 200)
        self.assertEqual(self.crear(stock_actual=0).status_code, 200)

    def test_entrada_html_se_escapa_en_pantalla(self):
        self.crear(nombre='<script>alert(1)</script>x')
        r = self.client.get(reverse('home'))
        self.assertNotContains(r, '<script>alert(1)</script>')

    def test_busqueda_con_comillas_no_rompe(self):
        self.entrar()
        r = self.client.get(reverse('home'), {'q': "' OR 1=1 --"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['page_obj']), 0)


class MovimientoTests(BaseTest):
    def mover(self, tipo, cantidad, motivo=None):
        self.entrar()
        motivo = motivo or ('COMPRA' if tipo == 'ENTRADA' else 'VENTA')
        return self.client.post(reverse('movimiento_crear'), {
            'producto': self.producto.pk, 'tipo': tipo, 'motivo': motivo, 'cantidad': cantidad})

    def test_entrada_suma_stock_y_registra_historial(self):
        self.assertEqual(self.mover('ENTRADA', 5).status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 15)
        m = Movimiento.objects.get()
        self.assertEqual((m.tipo, m.cantidad, m.usuario), ('ENTRADA', 5, self.ana))

    def test_salida_descuenta_stock(self):
        self.mover('SALIDA', 4)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 6)

    def test_salida_mayor_al_stock_se_rechaza(self):
        r = self.mover('SALIDA', 11)
        self.assertEqual(r.status_code, 200)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 10)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_cantidad_cero_negativa_o_excesiva(self):
        for c in [0, -3, 101]:
            self.assertEqual(self.mover('ENTRADA', c).status_code, 200)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_producto_con_movimientos_no_se_elimina(self):
        self.mover('ENTRADA', 1)
        self.client.post(reverse('producto_eliminar', args=[self.producto.pk]))
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_alerta_de_stock_minimo_en_inicio(self):
        self.mover('SALIDA', 8)
        r = self.client.get(reverse('inicio'))
        self.assertIn(self.producto, r.context['por_acabarse'])


class HistorialTests(BaseTest):
    def test_historial_lista_y_filtra(self):
        self.entrar()
        otro = Producto.objects.create(nombre='Aceite corporal', stock_actual=5, stock_minimo=1, usuario=self.ana)
        for prod in (self.producto, otro):
            self.client.post(reverse('movimiento_crear'), {
                'producto': prod.pk, 'tipo': 'ENTRADA', 'motivo': 'COMPRA', 'cantidad': 2})
        r = self.client.get(reverse('historial'))
        self.assertEqual(len(r.context['page_obj']), 2)
        r = self.client.get(reverse('historial'), {'producto': otro.pk})
        self.assertEqual(len(r.context['page_obj']), 1)

    def test_historial_requiere_login(self):
        r = self.client.get(reverse('historial'))
        self.assertEqual(r.status_code, 302)


class CabecerasSeguridadTests(BaseTest):
    def test_cookie_de_sesion_httponly_y_csrf_activo(self):
        self.client.post(reverse('login'), {'username': 'ana', 'password': 'ClaveSegura#2026'})
        self.assertTrue(self.client.cookies['sessionid']['httponly'])

    def test_post_sin_token_csrf_es_rechazado(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        r = c.post(reverse('login'), {'username': 'ana', 'password': 'ClaveSegura#2026'})
        self.assertEqual(r.status_code, 403)

    def test_cabecera_anti_clickjacking(self):
        r = self.client.get(reverse('login'))
        self.assertEqual(r.headers.get('X-Frame-Options'), 'DENY')
