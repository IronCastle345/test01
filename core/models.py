from django.db import models


class parle(models.Model):
    nombre = models.CharField(max_length=200,null=True,blank=True,default="Nuevo Parle")
    cant_cajas = models.IntegerField(default=0)
    pos_x = models.IntegerField(default=0)  # Posición en el eje X
    pos_y = models.IntegerField(default=0)  # Posición en el eje Y
    ancho = models.IntegerField(default=200)  # Ancho del cuadrado
    alto = models.IntegerField(default=150)  # Alto del cuadrado

    def __str__(self):
        return f"{self.nombre}"

class caja(models.Model):
    nombre = models.CharField(max_length=200, null=True,blank=True)
    id_parle = models.ForeignKey(parle, on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Parle asociado")
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