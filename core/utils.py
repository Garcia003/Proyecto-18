from django.core.mail import EmailMessage

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