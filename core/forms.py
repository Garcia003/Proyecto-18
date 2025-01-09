from django import forms
from .models import *
from .utils import sendMailNotifications

def custom_style(fields):
    for field in fields:
        widget = fields[field].widget
        apply_class(widget)

def apply_class(widget):
    widget.attrs.update({'class': 'form-control'})
    if widget.__class__.__name__ == 'Select':
        widget.attrs.update({'class': 'form-select w-100'})

class MailForm(forms.ModelForm):
    class Meta:
        model= Mail
        exclude = ['payment_point']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',  # Selector de calendario
                'class': 'form-control',  # Estilo adicional
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        custom_style(self.fields)

    def save(self, commit = True):
        mail = super().save(commit=False)
        if mail:
            mail.save()
            mail_subject = '¡Gracias por tu compra!'
            from_email = 'dtecnologia99@gmail.com'
            message = f"""
            Hola {self.cleaned_data.get('name', 'Usuario')}, 
            
            ¡Gracias por realizar tu compra con nosotros!
            
            Aquí tienes los detalles de tu compra:
            - Producto: plan teleasistencia
            - Fecha: {self.cleaned_data.get('birth_date', 'No especificada')}
            
            Si tienes alguna pregunta o necesitas soporte, no dudes en contactarnos."""

            to_email = [self.cleaned_data['email']]
            try:
                sendMailNotifications(mail_subject, from_email, message, to_email)
            except Exception as e:
                print('Error: ', e)

        return mail
    

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model= Beneficiario
        exclude = ['mail']
        widgets = {
            'beneficiary_birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(BeneficiarioForm, self).__init__(*args, **kwargs)
        custom_style(self.fields)