from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('movimiento/', views.movimiento_crear, name='movimiento_crear'),
    path('productos/', views.home, name='home'),
    path('mis-productos/', views.mis_productos, name='mis_productos'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('producto/nuevo/', views.producto_crear, name='producto_crear'),
    path('producto/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('producto/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('grupos/', views.grupos, name='grupos'),
    path('registro/', views.registro, name='registro'),
    path('cuenta/', views.perfil, name='perfil'),
    path('cuenta/password/', views.CambiarPasswordView.as_view(), name='cambiar_password'),
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]