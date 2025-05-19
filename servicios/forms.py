from django.forms import ModelForm, ChoiceField, Select
from .models import Servicios
from django.forms import DateInput

class ContactForm(ModelForm):
    # Opciones para el servicio
    OPCIONES_SERVICIO = [
        ('Corte', 'Corte'),
        ('Barba + Corte', 'Barba + Corte'),
        ('Barba', 'Barba'),
        ('Ceja', 'Ceja'),
        ('Contornos', 'Contornos'),
        ('Barba + Ceja', 'Barba + Ceja'),
        ('Barba + Ceja + Corte', 'Barba + Ceja + Corte'),
    ]
    
    # Opciones para método de pago
    OPCIONES_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia')
    ]

    # Opciones para el barbero
    OPCIONES_BARBERO = [
        ('Peter', 'Peter'),
        ('Frank', 'Frank'),
    ]

    # Campos tipo select
    service = ChoiceField(choices=OPCIONES_SERVICIO, widget=Select(attrs={'class': 'form-select'}))
    payment_method = ChoiceField(choices=  OPCIONES_PAGO, widget=Select(attrs={'class': 'form-select'}))
    barber = ChoiceField(choices=OPCIONES_BARBERO, widget=Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Servicios
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args,  **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'Select':
                field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['date'].widget = DateInput(attrs={
            'type': 'date',
            'class': 'form-contrl'
        })