from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, related_name='productos', null=True, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, related_name='productos', blank=True)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='productos', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    TIPOS = [('ENTRADA', 'Entrada'), ('SALIDA', 'Salida')]
    MOTIVOS = [('COMPRA', 'Compra'), ('VENTA', 'Venta'), ('USO_INTERNO', 'Uso interno')]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    motivo = models.CharField(max_length=15, choices=MOTIVOS)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo} {self.cantidad} x {self.producto}'