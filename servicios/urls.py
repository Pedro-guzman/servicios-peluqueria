from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='servicios'),
    path('view/<int:id>', views.view, name='servicio_view'),
    path('edit/<int:id>', views.edit, name='servicio_edit'),
    path('create/', views.create, name='servicio_create'),
    path('delete/<int:id>', views.delete, name='servicio_delete'),
    path('dashboard/', views.dashboard, name='servicio_dashboard'),
    path('<letter>', views.index, name='servicios')
]
