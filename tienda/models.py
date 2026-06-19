from django.db import models
from django.db import models
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(
        upload_to='productos/'
    )
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.nombre


    categoria = models.CharField(
        max_length=50,
        default='Otros'
    )

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

    def __str__(self):
        return f"{self.producto.nombre}"
    
