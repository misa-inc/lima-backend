from django.core.mail import EmailMessage
from string import digits, ascii_lowercase, ascii_uppercase
from secrets import choice as secret_choice
from random import choice as random_choice
from os.path import basename, splitext

import threading
import uuid


MONTH = {1:"January", 2:"February", 3:"March", 4:"April", 
         5:"May", 6:"June", 7:"July", 8:"August", 
         9:"September", 10:"October", 11:"November", 12:"December"}
         
def get_filename_ext(filepath):
    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"blogs/{final_name}"


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def slug_generator(size: int = 10, char: str = digits + ascii_uppercase + ascii_lowercase) -> str:
    return "".join(random_choice(char) for _ in range(size))


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))


def get_random_code():
    code = str(uuid.uuid4())[:8].replace("-", " ").lower()
    return code


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = 'html'
        EmailThread(email).start()

