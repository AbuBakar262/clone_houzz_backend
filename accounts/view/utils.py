import random
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from houzzhub import settings


def generate_six_length_random_number():
    random_otp = random.SystemRandom().randint(100000, 999999)
    return str(random_otp)


def email_sender(email_info):
    subject = email_info.get('subject')
    message = email_info.get('message')
    host_email = settings.EMAIL_HOST_USER
    recipient_list = email_info.get('to_email')
    send_mail(subject, message, host_email, [recipient_list])


def phone_sender(phone_info):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_info.get('to_phone'),
        from_="+14092543785",
        body=phone_info.get('message'),
    )