from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class  Marca(models.Model):
    nombre_marca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_marca

class Producto(models.Model):
    codigo = models.CharField(max_length=6, null=True)
    nombre_producto = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()
    imagen = models.ImageField(upload_to="productos", null=True)
    Stock = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre_producto

opciones_consultas = [
    [0, "consulta"],
    [1, "reclamo"],
    [2, "sugerencia"],
    [3, "felicitaciones"]
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=datetime.now())
    cliente = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total = models.IntegerField()
    estado = models.CharField(max_length=20, default="EN PREPARACION")
    
    def __str__(self):
        return str(self.id)+" "+str(self.cliente.username)+" "+str(self.fecha)[0:20]

class Detalleventa(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    venta = models.ForeignKey(to=Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(to=Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return str(self.id)+" - "+self.producto.nombre_producto[0:20]+" "+str(self.venta.id)


