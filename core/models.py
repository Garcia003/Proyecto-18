from django.db import models
from .utils import method_payment, holder

from django.db import models
from .utils import method_payment, holder

from django.db import models
from .utils import method_payment, holder

class Mail(models.Model):
    document = models.CharField('Cédula', max_length=255)
    name = models.CharField('Nombres', max_length=255)
    last_name = models.CharField('Apellidos', max_length=255)
    birth_date = models.DateField('Fecha de Nacimiento')
    phone = models.CharField('Celular', max_length=255)
    email = models.EmailField('Correo Electrónico(Opcional)', max_length=255, blank=True, null=True)
    method_payment = models.CharField('Forma de Pago', max_length=255, choices=method_payment)
    holder = models.CharField('¿El Plan es para el Titular?', max_length=255, choices=holder)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.last_name}"


class Beneficiario(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)
    beneficiary_document = models.CharField('Cédula', max_length=255)
    beneficiary_name = models.CharField('Nombres', max_length=255)
    beneficiary_last_name = models.CharField('Apellidos', max_length=255)
    beneficiary_birth_date = models.DateField('Fecha de Nacimiento')
    beneficiary_phone = models.CharField('Celular', max_length=255)
    beneficiary_email = models.EmailField('Correo Electrónico(Opcional)', max_length=255, blank=True, null=True)
    beneficiary_relationship = models.CharField('Parentesco con el Titular', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.beneficiary_name} - {self.beneficiary_last_name}"
