import pika
import os
import ssl
import smtplib


def format_message(body):   #Decodifica el binario a string
    return body.decode("utf-8")

def listarqueue(ch, method, properties, body):
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles')
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    enviar_correo(files)
    return 

def encontrarqueue(ch, method, properties, body):
    search_files = format_message(body)
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles')
    files_found = [f for f in os.listdir(folder_path) if f.lower() in search_files and os.path.isfile(os.path.join(folder_path, f))]
    enviar_correo(files_found)
    return 



def enviar_correo(response):
        context = ssl.create_default_context()
        subject = 'Respuesta MOM'
        message = 'Error en el servicio gRPC, se tramito la solicitud via MOM, la  respuesta de la consulta es\n' + str(response)
        message = 'Subject: {}\n\n{}'.format(subject, message)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login('observatorioproyecto1@gmail.com', os.environ['passcorreo'])
        server.sendmail('observatorioproyecto1@gmail.com', 'dgonza45@eafit.edu.co', message)
        server.quit()
        return

# Escucha
connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['rabbithost'], 5672,'/', pika.PlainCredentials(os.environ['user'], os.environ['password'])))
channel = connection.channel()
channel.queue_declare(queue='listarqueue', durable=True)
channel.basic_consume(queue='listarqueue', on_message_callback=listarqueue, auto_ack=True)

channel.queue_declare(queue='encontrarqueue', durable=True)
channel.basic_consume(queue='encontrarqueue', on_message_callback=encontrarqueue, auto_ack=True)
channel.start_consuming()