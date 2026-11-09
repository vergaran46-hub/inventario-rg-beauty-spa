from django.contrib import admin
from .models import Categoria, Etiqueta, Producto, Movimiento

admin.site.register(Categoria)
admin.site.register(Etiqueta)
admin.site.register(Producto)
admin.site.register(Movimiento)