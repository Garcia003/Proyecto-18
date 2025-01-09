from django.core.mail import EmailMessage
import requests

from io import BytesIO
from PIL import Image, ImageDraw
import random
import qrcode

method_payment = [
    ('1', 'Anual'),
    ('2', 'Semestral'),
]

holder = [
    ('Si', 'Si'),
    ('No', 'No'),
]

def sendMailNotifications(mail_subject, from_email, message, to_email):
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.send()

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    
    return ip

def location(request):
    access_token = '06f6551cc2c21a' 
    ip = get_client_ip(request)
    # ip = '181.204.71.85'
    # ip = '190.249.156.186'
    # ip = '5.188.62.140' # Rusia 
    # ip = '157.100.143.51' # Ecuador 
    response = requests.get(f'https://ipinfo.io/{ip}/json?token={access_token}')
    data = response.json()
    print(data)
    return {
        'city': data['city'],
        'region': data['region'],
        'country': data['country'],
    }

# importar request
def generateslugid():
    caracteres = list('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    slugid = ''.join(random.choice(caracteres) for i in range(10))
    return slugid

def generateQRCode(qrid):
    # url = f'http://127.0.0.1/qrcode/{qrid}/'
    url = f'https://plataformas.48hoorassdia.com/uqr/qrcode/{qrid}/'
    qr_image = qrcode.make(url)
    fname = f'qrcode-{qrid}.png'
    buffer = BytesIO()
    qr_image.save(buffer, 'PNG')
    return fname, buffer

def OperatingSystem(request):
    user_agent = request.user_agent
    os = f'{user_agent.os.family} {user_agent.os.version_string}' if user_agent.is_pc else user_agent.os.family
    return {
        'os': os
    }

def getPercentajeValue(dictionary):
    total = sum(dictionary.values())
    dictionary = {
        key: {
        'value': count,
        'percentage': (count / total) * 100
        } for key, count in dictionary.items()
    }

    return dictionary
