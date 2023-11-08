## info de la materia: ST0263 <Tópicos Especiales en Telemática>
#
## Estudiante(s): Daniel Gonzalez Bernal, dgonza45@eafit.edu.co
#
## Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.com
#
## RETO #2 - Procesos comunicantes por API REST, RPC y MOM
#
## 1. breve descripción de la actividad:
Se diseñaron e implementarion 2 microservicios ofrecidos por medio de un apiGateway, un servicio se comunica por un middleware gRPC y el otro por un middleware MOM, El servidor API Gateway, utilizará como comunicación principal con los servidores de los microservicios la comunicación gRPC, y en caso de fallo con estos servidores, deberá utilizar la comunicación MOM para enviar la solicitud y enviar respuesta de la peticion.
#
## 1.1. Que se logro: 
Se diseñaron e implementaron correctamente todos los servicios y servidores propuestos, se utilizo una ip elastica para la entrada de solicitudes via HTTP segun fue solicitado. Todo el sistema gRPC y MOM funcionan al igual que el apiGateway.
#
## 1.2. Que falto: 
Todo el trabajo fue completado segun las instruccion dadas.
#
## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizo Flask para visualizar las respuestas del servidor utilizando HTTP, se crearon 4 servidores en AWS y se configuraron de la siguiente manera: Un servidor como apiGateway con IP elasica, un servidor que recibe solicitudes gRPC y las ejecute, un servidor corriendo RabbitMQ como servicio MOM, y un ultimo servidor que ejecuta las solicitudes encoladas en el MOM y envia respuesta de la solicitud via correo electronico.
#
## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
#
 Debido a que todo el codigo esta escrito en python no es necesario compilar, sin embargo, el archivo .proto del gRPC si es necesario compilarlo para que funcione correctamente, esto se hace con el siguiente codigo:
#
sudo python3 -m grpc_tools.protoc -I ../protobufs --python_out=. --pyi_out=. --grpc_python_out=. ../protobufs/contrato.proto
#
## Las librerias adicionales que se utilizaron son las siguientes:
1. Flask: Carga y renderizado de las respuestas del servidor con .html. 
2. os: Se utilizo para el manejo y busqueda de archivos en el servidor.
3. grpc: Manejo de la mensajeria gRPC.
4. pika: Manejo de RabbitMQ (Comunicacion MOM).
5. sll: Permite comunicarse de forma segura con el servidor de correo.
6. smtplib: Permite crear una sesion SMTP para el envio de correos.
#
## La configuracion de las variables de ambiente se realizo con los siguientes codigos:
1. export hostip = 172.31.46.195
2. export hostport = 8080
3. export grpcipport = 172.31.38.44:50051
4. export rabbithost=34.201.203.162
5. export user=user (Usuario de rabbitMQ)
6. export password=password (Password de rabbitMQ)
7. export passcorreo= (Esta KEY es secreta)
#
## Como configuracion de directorios tenemos el siguiente arbol de directorios:
#
Caperta Reto2
#
Directorio: apiGateway
1. protobufs.
2. src ( En esta carpeta se encuentra el archivo para iniciar el server "apiGateway.py" ).
2.1. templates.
#
 Directorio: gRPC
1. protobufs
2. src ( En esta carpeta se encuentra el archivo para iniciar el server "gRPC.py" )
3. serverFiles
#
 Directorio: server2
1. src ( En esta carpeta se encuentra el archivo para iniciar el server "server2.py" )
2. serverFiles
#
#
## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
#
## Se utilizaron las siguientes direcciones IP:
1. IP DE ENTRADA= 44.217.252.126 (Elastica)
2. IP del rabbitmq host= 34.201.203.162 (Elastica)
3. ip host privada = 172.31.46.195:8080
4. ip grppc privada = 172.31.38.44:50051
#
Para correr el proyecto se deben primero configurar las variables de entorno que se muestran en la parte de arriba e importar todas las librerias, mas adelante solo el necesario correr cada uno los archivos .py en su respectivo servidor que tiene el mismo nombre. En caso de tener 4 servidores sin configurar, solo es necesario correr cada uno de los archivos de servidor en cada servidor y en el cuarto configurar utilizando docker un servidor para los mensajes de RabbitMQ


## Mini guia de como un usuario utilizaría el software o la aplicación
#
Para solicitar los servicios solo es necesario utilizar la herramienta Postman de la siguiente manera:
1. GET a la direccion 44.217.252.126:8080/listar_archivos para listar todos los archivos en el servidor.
2. POST a la direccion 44.217.252.126:8080/encontrar_archivos , en el body del mensaje se selecciona la opcion form-data, y en el formulario se llena en "key" con la palabra filelist y en "value" el nombre del archivo a mostrar, el servidor retornara entonces una lista de todos los archivos solicitados y otra lista de cuales de los archivos solicitados se encontraron copias en el servidor.
#
En caso de que el servidor gRPC no este disponible, la informacion se enviaria via MOM al servidor #2 que contiene copia de todos los archivos y retornara el resultado no por el archivo HTML sino via correo electronico. Ademas mostrara por un HTML un aviso de que la solicitud se envio al MOM.
#

# referencias:
1. https://github.com/st0263eafit/st0263-232/tree/main/Laboratorio-RPC
2. https://protobuf.dev/
3. https://grpc.io/
4. https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
5. https://www.velotio.com/engineering-blog/grpc-implementation-using-python

#### versión README.md -> 1.0 (2023-agosto)
