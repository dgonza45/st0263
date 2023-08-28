import pika
import os


def format_message(body):   #Decodifica el binario a string
    return body.decode("utf-8")

def listarqueue(ch, method, properties, body):
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles')
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(files)    #Imprime resultado
    return 

def encontrarqueue(ch, method, properties, body):
    search_files = format_message(body)
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles')
    files_found = [f for f in os.listdir(folder_path) if f.lower() in search_files and os.path.isfile(os.path.join(folder_path, f))]
    print(files_found)  #Imprime resultado
    return 


# Escucha
connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['rabbithost'], 5672,'/', pika.PlainCredentials(os.environ['user'], os.environ['password'])))
channel = connection.channel()
channel.queue_declare(queue='listarqueue', durable=True)
channel.basic_consume(queue='listarqueue', on_message_callback=listarqueue, auto_ack=True)

channel.queue_declare(queue='encontrarqueue', durable=True)
channel.basic_consume(queue='encontrarqueue', on_message_callback=encontrarqueue, auto_ack=True)
channel.start_consuming()