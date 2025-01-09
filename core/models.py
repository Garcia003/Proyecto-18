from django.db import models
from django.core.files import File
from django.contrib.sites.shortcuts import get_current_site
from .utils import method_payment, holder, generateQRCode, generateslugid


class PaymentPoint(models.Model):
    name = models.CharField(max_length=255)
    qrid = models.CharField(max_length=10, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_code', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.qrid:
            self.qrid = generateslugid()
            fname, buffer = generateQRCode(self.qrid)
            self.qr_code.save(fname, File(buffer), save=False)
            buffer.close()
    
        super().save(*args, **kwargs)

    

    def __str__(self):
        return self.name

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

    payment_point = models.ForeignKey(PaymentPoint, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.last_name}"


class Beneficiario(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, null=True, blank=True)
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

class QrTable(models.Model):
    point = models.ForeignKey(PaymentPoint, on_delete=models.CASCADE)
    url = models.URLField(max_length=250)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.point.name


class ReportQr(models.Model):
    qr_table = models.ForeignKey(QrTable, on_delete=models.CASCADE)
    country = models.CharField('Pais', max_length=100)
    city = models.CharField('Ciudad', max_length=100)
    device = models.CharField('Dispositivo', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.qr_table.point.name
    

