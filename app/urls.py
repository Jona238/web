from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('productos/', productos, name="productos"),
    path('somos/', somos, name="somos"),
    path('contacto', contacto, name="contacto"),
    path('perfil/', perfil, name="perfil"),
    path('carro/', carro, name="carro"),
    path('noticia_uno/', noticia_uno, name="noticia_uno"),
    path('noticia_dos/', noticia_dos, name="noticia_dos"),
    path('noticia_tres/', noticia_tres, name="noticia_tres"),
    path('agregar-producto/', agregar_producto, name="agregar_producto"),
    path('listar-productos/', listar_productos, name="listar_productos"),
    path('modificar-producto/<id>/', modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('registro/', registro, name="registro"),
    path('addtocar/<codigo>/', addtocar, name="addtocar"),
    path('dropitem/<codigo>/', dropitem, name="dropitem"),
    path('comprar', comprar, name="comprar"),
    path("historial", historial, name="historial"),
    path("suscribir",suscribir, name="suscribir"),
]