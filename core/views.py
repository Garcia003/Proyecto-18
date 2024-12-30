from django.shortcuts import render, redirect
import sweetify
from .models import Mail, Beneficiario
from .forms import MailForm, BeneficiarioForm

from django.shortcuts import render, redirect
import sweetify
from .models import Mail, Beneficiario
from .forms import MailForm, BeneficiarioForm

# def registrar_afiliacion(request):
#     data = {
#         'form': MailForm(),
#         'beneficiario_form': BeneficiarioForm()
#     }

#     if request.method == 'POST':
#         form = MailForm(request.POST)
#         if form.is_valid():
#             form_instace = form.save()
#             if form_instace.holder == 'No':
#                 beneficiario_form = BeneficiarioForm(request.POST)
#                 if beneficiario_form.is_valid():
#                     beneficiario_form.save()
#                     sweetify.success(request, 'Beneficiario registrado correctamente.')
#                 else:
#                     sweetify.success(request, 'Beneficiario no ha sido registrado correctamente.')
#                     data['beneficiario_form'] = BeneficiarioForm
#                     return redirect ('formulario')
#             else:
#                return redirect ('formulario') 
#         else:
#             data['form'] = form

#     return render(request, 'form.html', data)


def registrar_afiliacion(request, point=None):
    
    data = {
        'form': MailForm(),
        'beneficiario_form': BeneficiarioForm()
    }

    if request.method == 'POST':
        form = MailForm(request.POST)
        es_titular = request.POST.get('es_titular')

        if form.is_valid():
            form_instace = form.save(commit=False)



            if es_titular == 'Si':
                form_instace.save()
                sweetify.success(request, 'Beneficiario registrado correctamente.')                
                return redirect ('formulario')
            elif es_titular == 'No':
               Beneficiario_form = Beneficiario_form(request.POST)
               if Beneficiario_form.is_valid():
                    form_instace.save()
                    Beneficiario_instance = Beneficiario_form.save(commit=False)
                    Beneficiario_instance.mail = form_instace
                    Beneficiario_instance.save()
                    return redirect('formulario')
        else:
            data['form'] = form
            data['beneficiario_form'] = Beneficiario_form

    return render(request, 'form.html', data)