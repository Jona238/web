from django.contrib import admin
from .models import *
from .forms import ProductoForm
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre_producto", "precio", "nuevo", "marca"]
    list_editable = ["precio"]
    search_fields = ["nombre_producto"]
    list_filter = ["marca", "nuevo"]
    list_per_page = 5
    form = ProductoForm

class VentaAdmin(admin.ModelAdmin):
    list_display = ["id","fecha", "cliente", "total", "estado"]
    list_editable = ["estado"]
    search_fields = ["cliente"]
    
class DetalleAdmin(admin.ModelAdmin):
    list_display = ["id","venta", "producto", "cantidad", "precio"]
    search_fields = ["venta"]

admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Detalleventa,DetalleAdmin)
