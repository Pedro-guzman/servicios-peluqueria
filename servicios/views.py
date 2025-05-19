from django.shortcuts import render, redirect
from .models  import Servicios
from . forms import ContactForm
from django.http import HttpResponse
from django.contrib import messages
import plotly.graph_objs as go
import plotly.offline as opy
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime



def index(request, letter=None):
    if letter != None:
        servicios = Servicios.objects.filter(customer__istartswith=letter)
    else:
         servicios = Servicios.objects.filter(customer__contains=request.GET.get('search', ''))
    context = {
        'servicios': servicios
    }
    return render(request, 'servicios/index.html', context )

def view(request, id):
    servicio = Servicios.objects.get(id=id)
    context = {
        'servicio': servicio
    }
    return render(request, 'servicios/detail.html', context)

def edit(request, id):
    servicios = Servicios.objects.get(id=id)
    
    if (request.method == 'GET'):
        form = ContactForm(instance=servicios)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'servicios/edit.html', context )
    if (request.method == 'POST'):
        form = ContactForm(request.POST, instance=servicios)
        form.save()
        
        context = {
            'form': form,
            'id': id
        } 
        messages.success(request, "¡Servicio editado exitosamente!")    
        return render(request, 'servicios/edit.html', context)
    
 # Vista para añadir nuevos servicios   
def create(request):
        if(request.method == 'GET'):
            form = ContactForm()
            context = {
                'form': form,
            }
            return render(request, 'servicios/create.html', context)
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid:
                form.save()
                messages.success(request, 'Servicio agregado correctamente.')
                
            # Creamos un formulario nuevo para mostrarlo vacío de nuevo
            form = ContactForm()
        else:
            messages.error(request, 'Por favor corrige los errores.')

        return render(request, 'servicios/create.html', {'form': form})
        
# VIsta para borrar un servicio
def delete(request, id):
    servicio = Servicios.objects.get(id=id)
    servicio.delete()
    return redirect('servicios')

# Vista para hacer gráfica, servicios realizados
def dashboard(request):
    graficas = []

    # Capturamos fechas del GET
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    servicios = Servicios.objects.all()

    # Si hay fechas, aplicamos el filtro
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d")
            servicios = servicios.filter(date__range=(fecha_inicio_obj, fecha_fin_obj))
        except ValueError:
            pass  # Si las fechas son inválidas, no hacemos el filtro

    #  Servicios por tipo
    servicios_data = servicios.values('service').annotate(total=Count('id'))
    labels1 = [item['service'] for item in servicios_data]
    valores1 = [item['total'] for item in servicios_data]
    trace1 = go.Bar(x=labels1, y=valores1)
    fig1 = go.Figure(data=[trace1], layout=go.Layout(title='Servicios por tipo', yaxis=dict(tickformat='d')))
    graficas.append(opy.plot(fig1, auto_open=False, output_type='div'))

    #  Servicios por día
    servicios_dia = servicios.annotate(fecha=TruncDate('date')).values('fecha').annotate(total=Count('id')).order_by('fecha')
    labels2 = [str(item['fecha']) for item in servicios_dia]
    valores2 = [item['total'] for item in servicios_dia]
    trace2 = go.Bar(x=labels2, y=valores2)
    fig2 = go.Figure(data=[trace2], layout=go.Layout(title='Servicios por día', yaxis=dict(tickformat='d')))
    graficas.append(opy.plot(fig2, auto_open=False, output_type='div'))

    #  Porcentaje por peluquero
    servicios_peluquero = servicios.values('barber').annotate(total=Count('id'))
    labels3 = [item['barber'] for item in servicios_peluquero]
    valores3 = [item['total'] for item in servicios_peluquero]
    trace3 = go.Pie(labels=labels3, values=valores3)
    fig3 = go.Figure(data=[trace3], layout=go.Layout(title='Servicios por peluquero'))
    graficas.append(opy.plot(fig3, auto_open=False, output_type='div'))

    #  Porcentaje por método de pago
    pagos = servicios.values('payment_method').annotate(total=Count('id'))
    labels4 = [item['payment_method'] for item in pagos]
    valores4 = [item['total'] for item in pagos]
    trace4 = go.Pie(labels=labels4, values=valores4)
    fig4 = go.Figure(data=[trace4], layout=go.Layout(title='Métodos de pago'))
    graficas.append(opy.plot(fig4, auto_open=False, output_type='div'))

    return render(request, 'servicios/dashboard.html', {
        'graficas': graficas
    })