from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import caja

@receiver([post_save, post_delete], sender=caja)
def actualizar_contador_parle(sender, instance, **kwargs):
    if instance.id_parle:
        parle = instance.id_parle
        parle.cant_cajas = caja.objects.filter(id_parle=parle).count()
        parle.save()