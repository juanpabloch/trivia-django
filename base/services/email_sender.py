from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from django.template.loader import render_to_string
import ssl
import smtplib
import re

class EmailSender:
    def __init__(self, subject: str, sender: str, destination_list: list or tuple, template: str, template_data: dict = {}):

        exp_reg_email = r'^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$'

        # Validar que no sean vacios
        for key, value in locals().items():
            if key != 'self' and key != 'template_data' and not value:
                raise ValueError(f"El parámetro {key} es requerido")
            setattr(self, key, value)
        
        # Validar formato de correo electrónico
        if not re.match(exp_reg_email, sender):
            raise ValueError(f"El formato del correo electrónico '{sender}' del sender es inválido")
        
        # Validar tipo de datos de destination_list
        if not isinstance(destination_list, (list, tuple)):
            raise TypeError("destination_list debe ser una lista o tupla, de emails válidos")
        
        for email in destination_list:
            if not re.match(exp_reg_email, email):
                raise ValueError(f"El formato del correo electrónico {email} del destination_list es inválido ")
        
        #Se suelen hacer privados todos los atributos
        self.__subject = subject
        self.__sender = sender
        self.__destination_list=destination_list
        self.__template=template
        self.__template_data=template_data
        self.__password=""

    #Se generan metodos get PUBLICOS de los atributos 
    #que quieres que sean visibles.
    def get_subject(self) -> str:
        return self.__subject

    def get_sender(self) -> str:
        return self.__sender
    
    def get_destination_list(self) -> list or tuple:
        return self.__destination_list
    
    def get_template(self) -> str:
        return self.__template
    
    def get_template_data(self) -> dict:
        return self.__template_data

    #Se generan metodos set PUBLICOS de los atributos 
    #que quieres que sean visibles y MODIFICABLES
    def set_subject(self, subject: str) -> None:
        self.__subject = subject

    def set_sender(self, sender: str) -> None:
        self.__sender = sender

    def set_destination_list(self, destination_list: list or tuple) -> None:
        # Validar tipo de datos de destination_list
        if not isinstance(destination_list, (list, tuple)):
            raise TypeError("destination_list debe ser una lista o tupla")
        self.__destination_list = destination_list

    def set_template(self, template: str) -> None:
        self.__template = template

    def set_template_data(self, template_data: dict) -> None:
        self.__template_data = template_data

    def set_password(self, password: str) -> None:
        self.__password = password

    def send(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.get_subject()
        content = render_to_string(self.get_template(), self.get_template_data())

        # Create the plain-text and HTML version of your message
        text = f"""\
                {self.get_subject()}
                """

        # Turn these into plain/html MIMEText objects
        # part1 = MIMEText(text, "plain")
        part2 = MIMEText(content, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.__sender, self.__password)
            smtp.sendmail(self.get_sender(),
            self.get_destination_list(), message.as_string())