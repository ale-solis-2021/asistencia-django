from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateField()
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.alumno} - {self.fecha} - {'Presente' if self.presente else 'Ausente'}"
