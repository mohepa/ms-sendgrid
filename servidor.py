from flask import Flask, request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

print(__name__)

application = Flask(__name__)

@application.route('/')
def index():
    return "Bienvenido"

@application.route('/home')
def inicio():
    return {
        "status" : "ok",
        "code" :  200
    }        

@application.route('/cliente/<nombre>/<apellido>')
def cliente(nombre, apellido):
    return {
        "Nombre completo" :  nombre +  " "  + apellido
    }       

@application.route('/cliente/registro', methods=['POST'])
def registro():
    tipoContenido = request.content_type

    if( request.is_json ):
        datos = request.json

        return  {
            "to" :  datos  ["to"],
            "subject" :  datos  ["subject"],
            "message" :  datos  ["message"],
        }

    else:
        return  {
            "status" : "No es posible procesar su solicitud"
         }

@application.route('/enviarMail', methods =['POST'])
def enviarMail():

    message = Mail(
                from_email= os.environ.get('SENDGRID_SENDER_DRONENET'),
                to_emails='mapagusu@gmail.com',
                subject='Email enviado desde python DroneNet',
                html_content='<strong>Probando el envio de emails desde Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY_DRONENET'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return {
            "message" : "El email se envio con exito",
            "code" : response.status_code
        }

    except Exception as e:
        print(e)

        return {
            "message" : "No se pudo enviar el email",
            "error" : e
        }

if  __name__  ==  '__main__':
     application.run(host='127.0.0.1',  port=8000, debug=True)
