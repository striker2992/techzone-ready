from django.shortcuts import render, get_object_or_404
from .models import Producto, Pedido, DetallePedido
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def inicio(request):

    buscar = request.GET.get('buscar')
    categoria = request.GET.get('categoria')

    productos = Producto.objects.all()

    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )

    if categoria:
        productos = productos.filter(
            categoria=categoria
        )

    return render(
        request,
        'tienda/index.html',
        {'productos': productos}
    )


def producto(request, id):
    producto = get_object_or_404(Producto, id=id)


    return render(
    request,
    'tienda/producto.html',
    {'producto': producto}
)
def carrito(request):

    ids = request.session.get('carrito', [])

    productos = Producto.objects.filter(id__in=ids)

    total = sum(producto.precio for producto in productos)

    return render(
        request,
        'tienda/carrito.html',
        {
            'productos': productos,
            'total': total
        }
)



def agregar_carrito(request, id):

    carrito = request.session.get('carrito', [])

    carrito.append(id)

    request.session['carrito'] = carrito

    return redirect('carrito')
def eliminar_carrito(request, id):

    carrito = request.session.get('carrito', [])

def eliminar_carrito(request, id):

    carrito = request.session.get('carrito', [])

    if id in carrito:
        carrito.remove(id)

        request.session['carrito'] = carrito

        return redirect('carrito')

def registro(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')

    else:
        form = UserCreationForm(request.POST)

        for campo in form.fields.values():
            campo.help_text = ''

    return render(
        request,
        'registration/registro.html',
        {'form': form}
    )
from .models import Producto, Pedido

def finalizar_compra(request):

   
    ids = request.session.get('carrito', [])

    productos = Producto.objects.filter(
        id__in=ids
    )

    total = sum(
        producto.precio
        for producto in productos
    )

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total
    )

    for producto in productos:
        
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            precio=producto.precio
        )
        producto.stock -= 1
        producto.save()

    request.session['carrito'] = []

    return render(
        request,
        'tienda/compra_exitosa.html'
    )


@login_required(login_url='/accounts/login/')
def mis_compras(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-id')

    return render(
        request,
        'tienda/mis_compras.html',
        {
            'pedidos': pedidos
        }
    )

@login_required


@login_required
def panel_admin(request):

   
    if not request.user.is_staff:
        return redirect('/')

    total_productos = Producto.objects.count()
    total_usuarios = User.objects.count()
    total_pedidos = Pedido.objects.count()

    ventas_totales = sum(
        pedido.total
        for pedido in Pedido.objects.all()
    )

    return render(
        request,
        'admin_panel/dashboard.html',
        {
            'total_productos': total_productos,
            'total_usuarios': total_usuarios,
            'total_pedidos': total_pedidos,
            'ventas_totales': ventas_totales,
        }
    )
   
@login_required
def admin_productos(request):

    if not request.user.is_staff:
        return redirect('/')

    productos = Producto.objects.all()

    return render(
        request,
        'admin_panel/productos.html',
        {
            'productos': productos
        }
    )
@login_required
def admin_pedidos(request):


    if not request.user.is_staff:
        return redirect('/')

    pedidos = Pedido.objects.all().order_by('-id')

    return render(
        request,
        'admin_panel/pedidos.html',
        {
            'pedidos': pedidos
        }
    )




@login_required
def admin_usuarios(request):

    if not request.user.is_staff:
        return redirect('/')

    return render(
        request,
        'admin_panel/usuarios.html'
    )

@login_required
def crear_producto(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        if 'imagen' not in request.FILES:
            return render(
                request,
                'admin_panel/crear_producto.html',
                {'error': 'Debe seleccionar una imagen.'}
            )

        # Se guarda la categoría enviada por el formulario
        Producto.objects.create(
            nombre=request.POST['nombre'],
            precio=request.POST['precio'],
            descripcion=request.POST['descripcion'],
            imagen=request.FILES['imagen'],
            stock=request.POST['stock'],
            categoria=request.POST.get('categoria', 'Otros')  # <- Agregado
        )
        return redirect('admin_productos')

    return render(request, 'admin_panel/crear_producto.html')


@login_required
def editar_producto(request, id):
    if not request.user.is_staff:
        return redirect('/')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.precio = request.POST['precio']
        producto.descripcion = request.POST['descripcion']
        producto.stock = request.POST['stock']
        producto.categoria = request.POST.get('categoria', 'Otros')  # <- Agregado

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('admin_productos')

    return render(
        request,
        'admin_panel/editar_producto.html',
        {'producto': producto}
    )

@login_required
def eliminar_producto(request, id):


    if not request.user.is_staff:
        return redirect('/')

    producto = get_object_or_404(
        Producto,
        id=id
    )

    producto.delete()

    return redirect('admin_productos')




@login_required
def admin_usuarios(request):


    if not request.user.is_staff:
        return redirect('/')

    usuarios = User.objects.all()

    return render(
        request,
        'admin_panel/usuarios.html',
        {
            'usuarios': usuarios
        }
    )
@login_required
def cambiar_estado(request, id, estado):


    if not request.user.is_staff:
        return redirect('/')

    pedido = get_object_or_404(
        Pedido,
        id=id
    )

    pedido.estado = estado
    pedido.save()

    return redirect('admin_pedidos')
def contacto(request):
    return render(
    request,
    'tienda/contacto.html'
    )



