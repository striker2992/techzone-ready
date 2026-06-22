from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField(validators=[MinValueValidator(0)]) 
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.CharField(max_length=50, default='Otros')
    
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):


    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    total = models.IntegerField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )
    estado = models.CharField(
    max_length=20,
    default='Pendiente'
)

def __str__(self):
    return f"Pedido {self.pedido.id} - {self.producto.nombre}"

class DetallePedido(models.Model):

    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    precio = models.IntegerField()
    cantidad = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.producto.nombre}"
    
