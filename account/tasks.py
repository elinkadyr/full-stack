from celery import shared_task
from decouple import config
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404



@shared_task
def send_activation_code(email: str, code: str):
    message = ""
    html = f'''
<h1>для активации аккаунта нажмите на кнопку</h1>
<a href="{config('LINK')}api/v1/account/activate/{code}">
<button>Activate</button>
</a>
'''

    send_mail(
        subject="Активация аккаунта",
        message=message,
        from_email='a@gmail.com',
        recipient_list=[email],
        html_message=html
    )



@shared_task
def send_email_to_reset_password(email):
    from .models import MyUser
    user = get_object_or_404(MyUser, email=email)

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"{config('LINK')}api/v1/account/reset-password/{uidb64}/{token}"
    subject = "Set a New Password"
    message = f"Please reset your password using the following link: {link}."

    send_mail(
        subject, 
        message, 
        from_email='a@gmail.com', 
        recipient_list=[email],
        )

