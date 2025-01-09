from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Mail)
admin.site.register(Beneficiario)

@admin.register(PaymentPoint)
class PaymentPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'qrid', 'qr_code')

@admin.register(QrTable)
class QrTableAdmin(admin.ModelAdmin):
    list_display = ('point', 'url', 'count')

@admin.register(ReportQr)
class ReportQrAdmin(admin.ModelAdmin):
    list_display = ('qr_table', 'country', 'city', 'device', 'created_at')