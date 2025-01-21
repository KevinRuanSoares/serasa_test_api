from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from user.models import User


def send_password_reset_code(user: User):
    """
    Sends an email with a password reset code to a user.

    :param user: The user object to whom the email should be sent.
    """
    context = {'code': user.recover_password_code}
    message = get_template('Layouts/email/password_reset_code.html').render(context)
    subject = _('Your code to generate a new password!')
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'
    email.send()
