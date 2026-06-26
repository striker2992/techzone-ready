from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Producto, Pedido, DetallePedido
from .forms import RegistroUsuarioForm


def inicio(request):
    buscar = request.GET.get('buscar')
    categoria = request.GET.get('categoria')

    productos = Producto.objects.filter(activo=True)

    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )

    if categoria:
        productos = productos.filter(categoria=categoria)

    return render(request, 'tienda/index.html', {'productos': productos})

def producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'tienda/producto.html', {'producto': producto})

def contacto(request):
    return render(request, 'tienda/contacto.html')



def carrito(request):
    carrito = request.session.get('carrito', {})
    if isinstance(carrito, list): carrito = {}
        
    productos_carrito = []
    total = 0

    for id_str, cantidad in carrito.items():
        producto = Producto.objects.filter(id=int(id_str)).first()
        if producto:
            subtotal = producto.precio * cantidad
            total += subtotal
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

    return render(request, 'tienda/carrito.html', {
        'productos_carrito': productos_carrito,
        'total': total
    })
    
@login_required(login_url='registro')
def agregar_carrito(request, id):
    
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('inicio')
        
    carrito = request.session.get('carrito', {})
    if isinstance(carrito, list): carrito = {} 
        
    id_str = str(id)
    if id_str in carrito:
        carrito[id_str] += 1 
    else:
        carrito[id_str] = 1 
        
    request.session['carrito'] = carrito
    return redirect('carrito')

def eliminar_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if isinstance(carrito, list): carrito = {}
        
    id_str = str(id)
    if id_str in carrito:
        del carrito[id_str] 
        request.session['carrito'] = carrito
        
    return redirect('carrito')

@login_required(login_url='/accounts/login/')
def finalizar_compra(request):

    if request.user.is_staff:
        return redirect('inicio')
        
    carrito = request.session.get('carrito', {})
    if isinstance(carrito, list): carrito = {}
    
  
    if not carrito:
        return redirect('carrito')

    total = 0
    productos_a_comprar = []

    for id_str, cantidad in carrito.items():
        producto = Producto.objects.filter(id=int(id_str)).first()

        if producto:
            total += producto.precio * cantidad
            productos_a_comprar.append({
                'producto': producto,
                'cantidad': cantidad
            })

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total
    )

    for item in productos_a_comprar:
        producto = item['producto']
        cantidad = item['cantidad']

        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            precio=producto.precio,
            cantidad=cantidad
        )

        producto.stock -= cantidad
        producto.save()

    request.session['carrito'] = {}

    return render(request, 'tienda/compra_exitosa.html')

@login_required(login_url='/accounts/login/')
def mis_compras(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-id')
    return render(request, 'tienda/mis_compras.html', {'pedidos': pedidos})



def registro(request):
    if request.method == 'POST':

        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
    
        form = RegistroUsuarioForm()
        for campo in form.fields.values():
            campo.help_text = ''

    return render(request, 'registration/registro.html', {'form': form})



@login_required
def panel_admin(request):
    if not request.user.is_staff:
        return redirect('/')

    
    total_productos = Producto.objects.filter(activo=True).count()
    
    total_usuarios = User.objects.count()
    total_pedidos = Pedido.objects.count()

    ventas_totales = sum(pedido.total for pedido in Pedido.objects.all())

    return render(request, 'admin_panel/dashboard.html', {
        'total_productos': total_productos,
        'total_usuarios': total_usuarios,
        'total_pedidos': total_pedidos,
        'ventas_totales': ventas_totales,
    })
   
@login_required
def admin_productos(request):

    productos = Producto.objects.filter(activo=True)
    
    return render(request, 'admin_panel/productos.html', {'productos': productos})
@login_required
def admin_pedidos(request):
    if not request.user.is_staff:
        return redirect('/')

    pedidos = Pedido.objects.all().order_by('-id')
    return render(request, 'admin_panel/pedidos.html', {'pedidos': pedidos})

@login_required
def admin_usuarios(request):
    if not request.user.is_staff:
        return redirect('/')

    usuarios = User.objects.all()
    return render(request, 'admin_panel/usuarios.html', {'usuarios': usuarios})

@login_required
def crear_producto(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        precio = float(request.POST.get('precio', 0))
        stock = int(request.POST.get('stock', 0))
        
        if precio < 0 or stock < 0:
            return render(request, 'admin_panel/crear_producto.html', {
                'error': 'El precio y el stock no pueden ser negativos.'
            })
            
        if 'imagen' not in request.FILES:
            return render(request, 'admin_panel/crear_producto.html', {
                'error': 'Debe seleccionar una imagen.'
            })

        Producto.objects.create(
            nombre=request.POST['nombre'],
            precio=request.POST['precio'],
            descripcion=request.POST['descripcion'],
            imagen=request.FILES['imagen'],
            stock=request.POST['stock'],
            categoria=request.POST.get('categoria', 'Otros') 
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
        producto.categoria = request.POST.get('categoria', 'Otros')

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('admin_productos')

    return render(request, 'admin_panel/editar_producto.html', {'producto': producto})

@login_required
def eliminar_producto(request, id):
    if not request.user.is_staff:
        return redirect('/')
        
    producto = Producto.objects.get(id=id)
    producto.activo = False
    producto.save()
    
    return redirect('admin_productos')

@login_required
def cambiar_estado(request, id, estado):
    if not request.user.is_staff:
        return redirect('/')

    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = estado
    pedido.save()

    return redirect('admin_pedidos')
