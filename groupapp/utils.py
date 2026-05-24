from django.core.mail import send_mail

def send_group_email(subject, message, recipients):
    send_mail(
        subject,
        message,
        "yourgmail@gmail.com",
        recipients,
        fail_silently=True
    )