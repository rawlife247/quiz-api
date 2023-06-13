from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_reset_email(email, token, name):
    subject = "Your account verification email"
    email_from = settings.EMAIL_HOST_USER

    html_template = 'reset_pass_email.html'
    html_message = render_to_string(html_template, context={'token': token, 'name': name})
    recipient_list = [email]

    try:
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return {"is_sent": True}
    except Exception as e:
        return {"is_sent": False, "message": f"An error occurred while sending the email: {str(e)}"}
