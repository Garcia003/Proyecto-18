from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum, Count



from .models import PaymentPoint, QrTable, ReportQr
from .forms import MailForm, BeneficiarioForm
from .utils import getPercentajeValue, location, OperatingSystem

import pandas as pd
import sweetify
import requests


def registrar_afiliacion(request, qrid=None):
    point = PaymentPoint.objects.filter(qrid=qrid).first()
    data = {
        'form': MailForm(),
        'beneficiario_form': BeneficiarioForm()
    }
    if request.method == 'POST':
        form = MailForm(request.POST)
        es_titular = request.POST.get('holder')

        if form.is_valid():
            form_instace = form.save()
            if es_titular == 'Si':
                sweetify.success(request, 'Beneficiario registrado correctamente.')                
            elif es_titular == 'No':
               beneficiario_form = BeneficiarioForm(request.POST)
               if beneficiario_form.is_valid():
                    beneficiario_instance = beneficiario_form.save()
                    beneficiario_instance.mail = form_instace
                    beneficiario_instance.save()
                    sweetify.success(request, 'Beneficiario registrado correctamente 2.')   
               else:
                   print(beneficiario_form.errors)
            
            form_instace.payment_point = point
            form_instace.save()
            return redirect(request.path)

            
        else:
            data['form'] = form
            data['beneficiario_form'] = beneficiario_form

    return render(request, 'form.html', data)

def qrLink(request, qrid):
    print(request.path)
    point = PaymentPoint.objects.filter(qrid=qrid).first()
    if point:
        url = QrTable.objects.filter(point=point).first()
        url.count += 1
        url.save()


        os = OperatingSystem(request)
        locations = location(request)

        ReportQr.objects.create(
            qr_table=url,
            country=locations['country'],
            city=locations['city'],
            device=os['os']
        )

        return redirect(url.url)
    return JsonResponse({
        'error': 'qrid no existe'
    })


def importExcel(request):
    protocol = 'https' if request.is_secure() else 'http'
    domain = get_current_site(request).domain
    url_qr = f'{protocol}://{domain}'
    print(url_qr)
    if request.method == 'POST':
        print(request.POST)
        excel_file = request.FILES.get('file')
        path = excel_file.file
        df = pd.read_excel(path)
        for row in df.to_dict(orient='records'):
            try:
                point = PaymentPoint(**row)
                point.full_clean()
                point.save()

                url = reverse('formulario', kwargs={'qrid': point.qrid})
                url_complete = f'{url_qr}{url}'
                QrTable.objects.create(point=point,url= url_complete,)
            except Exception as e:
                print(e)
    return JsonResponse({
        'status': 'oki'
    })

def stats_general(request, qridd=None):
    total_qrs = QrTable.objects.all()
    total_sum = total_qrs.aggregate(total_sum= Sum('count'))
    scans = ReportQr.objects.all()
    if not qridd == None:
        total_qrs = total_qrs.filter(point__qrid=qridd)
        total_sum = total_qrs.aggregate(total_sum= Sum('count'))
        scans = ReportQr.objects.filter(qr_table__point__qrid=qridd)

        if not total_qrs:
            sweetify.error(request, 'QRID no existe')
            return redirect('stats_general')

    os_dict = {}
    countries_dict = {}
    cities_dict = {}
    qr_dict = {}
    for scan in scans:
        qrid = scan.qr_table.point.qrid
        name = scan.qr_table.point.name
        os_dict[scan.device] = os_dict.get(scan.device, 0) + 1
        countries_dict[scan.country] = countries_dict.get(scan.country, 0) + 1
        cities_dict[scan.city] = cities_dict.get(scan.city, 0) + 1
        qr_dict[f'{qrid}-{name}'] = qr_dict.get(f'{qrid}-{name}', 0) + 1


    os_dict = getPercentajeValue(os_dict)
    countries_dict = getPercentajeValue(countries_dict)
    cities_dict = getPercentajeValue(cities_dict)
    qr_dict = getPercentajeValue(qr_dict)


    data = {
        'title': 'Estadísticas',
        "subTitle": "Generales" if qridd == None else total_qrs.first(),
        'total_qrs': total_qrs.count(),
        'total_sum': total_sum['total_sum'],
        'reports': os_dict,
        'countries': countries_dict,
        'cities':cities_dict,
        'qr_dict':qr_dict,
    }
    return render(request, 'stats_general.html', data)