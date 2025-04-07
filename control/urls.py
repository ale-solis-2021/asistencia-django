from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/nuevo/', views.registrar_alumno, name='registrar_alumno'),
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('asistencia/', views.tomar_asistencia, name='tomar_asistencia'),
    path('asistencia/ver/', views.ver_asistencia, name='ver_asistencia'),
    path('asistencia/mes/<int:mes>/<int:anio>/', views.asistencia_por_mes, name='asistencia_por_mes'),
    path('asistencia/resumen/<int:anio>/', views.resumen_anual, name='resumen_anual'),
    path('alumnos/eliminar/<int:alumno_id>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('', views.inicio, name='inicio'),
    path('descargar/asistencia/<int:mes>/<int:anio>/', views.exportar_asistencia_mensual, name='descargar_asistencia_mensual'),
    path('descargar/asistencia/anual/<int:anio>/', views.exportar_asistencia_anual, name='descargar_asistencia_anual'),

    # 👉 Nueva ruta para registro de usuarios
    path('registro/', views.registro, name='registro'),
] 
