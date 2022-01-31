from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from GBDL1.settings import EMAIL_HOST_USER
import threading


class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()

    def join(self, timeout=None):
        """ Stopping the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)

class EmailThreadSimple(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg

    def join(self, timeout=None):
        """ Stopping the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)


def send_simple_text_email(subject, message, receivers):
    msg = send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        receivers,
        fail_silently=True
    )
    EmailThreadSimple(msg).start()


def send_html_email(subject, html_message, receivers):
    subject, from_email, to = subject, EMAIL_HOST_USER, receivers
    text_content = ''
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_message, "text/html")
    EmailThread(msg).start()