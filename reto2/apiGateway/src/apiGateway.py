from flask import Flask, render_template, request, redirect
import grpc
import contrato_pb2
import contrato_pb2_grpc
import os
import pika

app = Flask(__name__)



# Configuración del servidor gRPC
grpc_server_address = os.environ['grpcipport']  
channel = grpc.insecure_channel(grpc_server_address)
grpc_stub = contrato_pb2_grpc.FileListStub(channel)
grpc_stub2 = contrato_pb2_grpc.FindFileStub(channel)


# Configuracion de RabbitMQ 
rabbitmq_host =  os.environ['rabbithost']



#Funciones cuando se activa el MOM

def listar_to_rabbitmq(message):  # Funcion para enviar al rabbit solicitud de listar
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, 5672,'/', pika.PlainCredentials(os.environ['user'], os.environ['password'])))
    channel = connection.channel()
    channel.queue_declare(queue='listarqueue', durable=True)
    channel.basic_publish(exchange='', routing_key='listarqueue', body=message,  properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()
    return

def encontrar_to_rabbitmq(message): # Funcion para enviar al rabbit solicitud de encontrar
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, 5672,'/', pika.PlainCredentials(os.environ['user'], os.environ['password'])))
    channel = connection.channel()
    channel.queue_declare(queue='encontrarqueue', durable=True)
    channel.basic_publish(exchange='', routing_key='encontrarqueue', body=message,  properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()
    return



#Funciones para trabajar con gRPC

@app.route('/listar_archivos', methods=['GET'])    #Funcion gRPC para "listar archivos"
def listar_archivos():
    try:
        response = grpc_stub.ListFiles(contrato_pb2.Empty())
        files = response.files_found
        joined_string = ''.join(files)
        filenames = [filename for filename in joined_string.split('\n') if filename] # Organiza la respuesta para que se vea bien en HTML
        return render_template('listar_archivos.html', filenames=filenames)  # Envia la respuesta como un HTML para mostrar en el browser
    except grpc.RpcError as e:
        print("Error en el servidor gRPC:", e)
        listar_to_rabbitmq("listar_archivos")
        return render_template('MOM.html')


@app.route('/encontrar_archivos', methods=['POST'])  #Funcion gRPC para "listar archivos"
def encontrar_archivos():
    try:
        filelist = request.form.getlist('filelist')
        file_request = contrato_pb2.FileRequest(files=filelist)
        response = grpc_stub2.FindFiles(file_request)

        found_files = "\n".join(response.files_found)  # De aqui para abajo organiza la respuesta para que se vea bien en HTML
        found_files_list = found_files.split('\n')  
        formatted_list = []
        item = ""
        for char in found_files_list:
            if char != "":
                item += char
            else:
                if item != "":
                    formatted_list.append(item)
                    item = ""
        if item != "":
            formatted_list.append(item)
        data = {                                # En este diccionario se pone la lista orginal y la de encontrados, para mostrar en la respuesta
            'original_files': filelist,        
            'found_files': formatted_list
        }
        return render_template('encontrar_archivos.html', data=data)  # Envia la respuesta como un HTML para mostrar en el browser
    except grpc.RpcError as e:
        print("Error en el servidor gRPC:", e)
        encontrar_to_rabbitmq(str(filelist))
        return render_template('MOM.html')

if __name__ == '__main__':
    app.run(host=os.environ['hostip'], port=os.environ['hostport'], debug=True)   # Ip y cosas importantes como variables de entorno.



