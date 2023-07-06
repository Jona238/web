from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ContactoForm, ProductoForm, CustomerUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
import requests
# Create your views here.

def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    suscrito(request, data)
    return render(request, 'app/home.html', data)

def productos(request):

    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/productos.html',data)

def suscribir(request):
    data = {}
    
    if request.method == "POST":
        if request.user.is_authenticated:
            resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{request.user.email}")
            data["mensaje"] = resp.json()["mensaje"]
            suscrito(request,data)
        return render (request,'app/suscripcion.html', data)
    else: 
        suscrito(request,data)       
        return render (request,'app/suscripcion.html', data)

def suscrito(request,data):
    if request.user.is_authenticated:
        email = request.user.email
        resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{email}")
        data["suscrito"] = resp.json()["suscrito"]

def somos(request):
    return render(request, 'app/somos.html')

def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "contacto guardado"
        else:
            data["form"] = formulario
    return render(request, 'app/contacto.html', data)


def perfil(request):
    if not request.user.is_authenticated:
        return redirect(to="login")
    compras = Venta.objects.filter(cliente=request.user)
    return render(request, 'app/perfil.html', {"compras":compras})

@login_required
def carro(request):
    return render(request, 'app/carro.html', {"carro":request.session.get("carro", [])})

def noticia_uno(request):
    return render(request, 'app/noticia_uno.html')

def noticia_dos(request):
    return render(request, 'app/noticia_dos.html')

def noticia_tres(request):
    return render(request, 'app/noticia_tres.html')

@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form':  ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
            data["mensaje"] = "guardado correctamente"
        else:
            data["form"] = formulario
    return render(request, 'app/producto/agregar.html', data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }
    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="listar_productos")
        data["form"]= formulario
    return render(request, 'app/producto/modificar.html', data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_productos")

def registro(request):
    data = {
        'form': CustomerUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomerUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html',data)


def addtocar(request, codigo):
    producto = Producto.objects.get(codigo = codigo)         
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            item[3]+= 1
            item[4] = item[2] * item[3]
            break
    else:
        carro.append([codigo, producto.nombre_producto, producto.precio, 1, producto.precio])
    request.session["carro"] = carro
    return redirect(to="carro")

def comprar(request):
    if not request.user.is_authenticated:
        return redirect(to="login")
    carro = request.session.get("carro", [])
    total = 0
    for item in carro:
        total += item[4]
    venta = Venta()
    venta.cliente = request.user
    venta.total = total
    venta.save() 
    messages.success(request, "Compra realizada!.")
    for item in carro:
        nombre_producto = Detalleventa()
        nombre_producto.producto = Producto.objects.get(codigo = item[0])
        nombre_producto.precio = item[2]
        nombre_producto.cantidad = item[3]
        nombre_producto.venta = venta
        nombre_producto.save()
        
        nombre_producto.producto.Stock -= nombre_producto.cantidad
        nombre_producto.producto.save()
        request.session["carro"] = []
    return redirect(to="carro")

def historial(request):
    if not request.user.is_authenticated:
        return redirect(to="login")
    compras = Venta.objects.filter(cliente=request.user)
    return render(request, 'app/historial.html', {"compras":compras})

def dropitem(request, codigo):
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            if item[3] > 1:
                item[3] -= 1
                item[4] = item[2] * item[3]
                break
            else:
                carro.remove(item)
    request.session["carro"] = carro
    return redirect(to="carro")