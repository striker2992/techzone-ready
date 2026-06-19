from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('producto/<int:id>/', views.producto, name='producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar-carrito/<int:id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('registro/', views.registro, name='registro'),
    path('finalizar-compra/',views.finalizar_compra,name='finalizar_compra'),
    path('mis-compras/',views.mis_compras,name='mis_compras'),
    path('panel-admin/',views.panel_admin,name='panel_admin'),
    path('panel-admin/productos/',views.admin_productos,name='admin_productos'),
    path('panel-admin/pedidos/',views.admin_pedidos,name='admin_pedidos'),
    path('panel-admin/usuarios/',views.admin_usuarios,name='admin_usuarios'),
    path('panel-admin/productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('panel-admin/productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('panel-admin/productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('panel-admin/productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path(
        'panel-admin/pedidos/<int:id>/<str:estado>/',
        views.cambiar_estado,
        name='cambiar_estado'
    ),
    path(
        'contacto/',
        views.contacto,
        name='contacto'
        ),

]
