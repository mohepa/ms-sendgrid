from flask import Flask, jsonify, request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
import re

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

    tipoContenido = request.content_type
    if ( request.is_json ):
        
        datos = request.get_data()
        
        try:
            json.loads(datos)            
        except Exception as e:
            return jsonify(
                {
                    "message": "Los datos enviados no son un objeto Json",
                    "status" : "error"
                }
            )

        plantillaEmail = request.get_json()

        if( "to" not in plantillaEmail):
            return jsonify(
                {
                    "message": "No existe el campo to",
                    "status" : "error"
                }
            )
        if( "subject" not in plantillaEmail):
            return jsonify(
                {
                    "message": "No existe el campo subject",
                    "status" : "error"
                }
            )
        if( "message" not in plantillaEmail):
            return jsonify(
                {
                    "message": "No existe el campo message",
                    "status" : "error"
                }
            )




    #if( request.is_json ):
        #datos = request.json

        

        validacionMAil = re.match(r"^[a-z0-9]{3,20}@[a-z]{5,10}.[a-z]{2,3}$", plantillaEmail ["to"])
        if( validacionMAil == None):
            return jsonify (
                {
                "message" : "No es un email válido",
                "status" : "error"
                }
            )

        validacionSubject = re.match(r"^[A-Za-z0-9 \.\,]{3,500}$", plantillaEmail ["subject"])
        if( validacionSubject == None):
            return jsonify (
                {
                "message" : "El subject debe contener mínimo 3 caracteres",
                "status" : "error"
                }
            )

        validacionMessage = re.match(r"[A-Za-z0-9 \.\,]{3,500}$", plantillaEmail ["message"])
        if( validacionMessage == None):
            return jsonify (
                {
                "message" : "El campo message debe contener mínimo 3 caracteres",
                "status" : "error"
                }
            )

               
        message = Mail(
                from_email= os.environ.get('SENDGRID_SENDER_DRONENET'),
                to_emails=      plantillaEmail["to"],
                subject=        plantillaEmail["subject"],
                html_content=   plantillaEmail["message"])


            
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

            return jsonify(
                {
                    "message": "Ocurrio un error al enviar mail ",
                    "status" : "error"
                }
            )
    else:
        return jsonify({
            "message": "No se puede procesar su solicitud, ya que no esta en formato JSON",
            "status" : "error"
        })

if  __name__  ==  '__main__':
     application.run(host='127.0.0.1',  port=8000, debug=True)

