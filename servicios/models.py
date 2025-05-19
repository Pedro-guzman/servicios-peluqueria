from django.db import models
from datetime import date

class Servicios(models.Model):
    date = models.DateField(default=date.today) 
    customer = models.CharField(max_length=50, blank=False, null=False) 
    service = models.CharField(max_length=50, blank=False, null=False) 
    price = models.DecimalField(max_digits=7, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=False, null=False) 
    barber = models.CharField(max_length=50, blank=False, null=False) 
    
    def __str__(self):
        return f"Cliente: {self.customer}\n - Servicio: {self.service}\n - Fecha: {self.date}\n - Peluquero:  {self.barber}"
    