from django.shortcuts import render, redirect
from .forms import AlumnoForm, AsistenciaForm
from .models import Alumno, Asistencia
from django.utils.timezone import now

from django.db.models import Count, Q
import calendar
from datetime import date

from collections import defaultdict
from django.shortcuts import get_object_or_404

import pandas as pd
from django.http import HttpResponse
import calendar
from datetime import date


def registrar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'control/registrar_alumno.html', {'form': form})

def lista_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'control/lista_alumnos.html', {'alumnos': alumnos})

def tomar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_asistencia')
    else:
        form = AsistenciaForm(initial={'fecha': now().date()})
    return render(request, 'control/tomar_asistencia.html', {'form': form})

def ver_asistencia(request):
    asistencias = Asistencia.objects.select_related('alumno').order_by('-fecha')
    return render(request, 'control/ver_asistencia.html', {'asistencias': asistencias})

from django.shortcuts import render
from .models import Alumno, Asistencia
from datetime import date
import calendar

def asistencia_por_mes(request, mes=None, anio=None):
    if not anio:
        anio = date.today().year
    if not mes:
        mes = date.today().month

    alumnos = Alumno.objects.all()
    dias_del_mes = calendar.monthrange(anio, mes)[1]
    fechas_mes = [date(anio, mes, d) for d in range(1, dias_del_mes + 1)]

    # Asistencia por alumno
    datos_asistencia = []
    for alumno in alumnos:
        asistencias = Asistencia.objects.filter(
            alumno=alumno,
            fecha__month=mes,
            fecha__year=anio
        )

        asistencia_dict = {a.fecha: a.presente for a in asistencias}

        presentes = sum(1 for dia in fechas_mes if asistencia_dict.get(dia, False))
        porcentaje = round((presentes / len(fechas_mes)) * 100, 2)

        datos_asistencia.append({
            'alumno': alumno,
            'asistencias': asistencia_dict,
            'presentes': presentes,
            'total_dias': len(fechas_mes),
            'porcentaje': porcentaje,
        })

    # Navegación de meses
    mes_anterior = mes - 1 if mes > 1 else 12
    mes_siguiente = mes + 1 if mes < 12 else 1

    context = {
        'datos_asistencia': datos_asistencia,
        'fechas_mes': fechas_mes,
        'nombre_mes': calendar.month_name[mes],
        'anio': anio,
        'mes_anterior': mes_anterior,
        'mes_siguiente': mes_siguiente,
        'mes': mes,
    }

    return render(request, 'control/asistencia_por_mes.html', context)


def resumen_anual(request, anio=None):
    if not anio:
        anio = date.today().year

    alumnos = Alumno.objects.all()
    meses = range(3, 13)  # De marzo (3) a diciembre (12)

    resumen = []

    for alumno in alumnos:
        total_presente = 0
        total_dias = 0
        detalle = []

        for mes in meses:
            dias_mes = calendar.monthrange(anio, mes)[1]
            fechas_mes = [date(anio, mes, d) for d in range(1, dias_mes + 1)]

            asistencias = Asistencia.objects.filter(alumno=alumno, fecha__month=mes, fecha__year=anio)
            presente_mes = sum(1 for a in asistencias if a.presente)
            total_presente += presente_mes
            total_dias += len(fechas_mes)

            porcentaje_mes = round((presente_mes / len(fechas_mes)) * 100, 2)
            detalle.append({
                'mes': calendar.month_abbr[mes],
                'presentes': presente_mes,
                'total': len(fechas_mes),
                'porcentaje': porcentaje_mes
            })

        porcentaje_anual = round((total_presente / total_dias) * 100, 2) if total_dias else 0

        resumen.append({
            'alumno': alumno,
            'detalle': detalle,
            'total_presente': total_presente,
            'total_dias': total_dias,
            'porcentaje_anual': porcentaje_anual
        })

    return render(request, 'control/resumen_anual.html', {
        'resumen': resumen,
        'anio': anio,
    })
    

def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    return render(request, 'control/eliminar_alumno.html', {'alumno': alumno})

def inicio(request):
    return render(request, 'control/inicio.html')

def exportar_asistencia_mensual(request, mes, anio):
    alumnos = Alumno.objects.all()
    dias_mes = calendar.monthrange(anio, mes)[1]
    fechas = [date(anio, mes, d) for d in range(1, dias_mes + 1)]

    data = []

    for alumno in alumnos:
        fila = {'Alumno': str(alumno)}
        asistencias = Asistencia.objects.filter(alumno=alumno, fecha__month=mes, fecha__year=anio)
        asistencias_dict = {a.fecha: 'P' if a.presente else 'A' for a in asistencias}
        for f in fechas:
            fila[f.day] = asistencias_dict.get(f, '-')
        data.append(fila)

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=asistencia_{anio}_{mes}.xlsx'
    df.to_excel(response, index=False)
    return response

def exportar_asistencia_anual(request, anio):
    alumnos = Alumno.objects.all()
    meses = range(3, 13)
    data = []

    for alumno in alumnos:
        fila = {'Alumno': str(alumno)}
        for mes in meses:
            dias_mes = calendar.monthrange(anio, mes)[1]
            fechas_mes = [date(anio, mes, d) for d in range(1, dias_mes + 1)]
            asistencias = Asistencia.objects.filter(alumno=alumno, fecha__month=mes, fecha__year=anio)
            presentes = sum(1 for a in asistencias if a.presente)
            fila[calendar.month_abbr[mes]] = f'{presentes}/{len(fechas_mes)}'
        data.append(fila)

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=asistencia_anual_{anio}.xlsx'
    df.to_excel(response, index=False)
    return response
