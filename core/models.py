from django.db import models

# Create your models here.
class parle(models.Model):
    nombre = models.CharField(max_length=200,null=True,blank=True)
    cant_cajas = models.IntegerField()

    def __str__(self):
        return f"{self.nombre}"

class caja(models.Model):
    nombre = models.CharField(max_length=200, null=True,blank=True)
    id_parle = models.ForeignKey(parle, on_delete=models.SET_NULL,null=True,blank=True)
    cant_piezas = models.IntegerField()

    def __str__(self):
        return f"{self.nombre}"

class tipo_de_pieza(models.Model):
    nombre = models.CharField(max_length=200,null=True,blank=True)
    tipo = models.CharField(max_length=200,null=True,blank=True)
    id_caja = models.ForeignKey(caja,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})" 

class pieza(models.Model):
    codigo = models.CharField(
        max_length=40,
        unique=True,  # Garantiza que no haya duplicados
        verbose_name="Código único",
        null=True,
        blank=True,
    )
    nombre = models.CharField(max_length=200,null=True,blank=True)
    tipo = models.CharField(max_length=200,null=True,blank=True)
    id_caja = models.ForeignKey(caja,on_delete=models.CASCADE,related_name="piezas")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"