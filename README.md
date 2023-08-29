# info de la materia: ST0263 <Tópicos Especiales en Telemática>
#
# Estudiante(s): Daniel Gonzalez Bernal, dgonza45@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.com
#
# RETO #2 - Procesos comunicantes por API REST, RPC y MOM
#
## 1. breve descripción de la actividad:
Se diseñaron e implementarion 2 microservicios ofrecidos por medio de un apiGateway, un servicio se comunica por un middleware gRPC y el otro por un middleware MOM, El servidor API Gateway, utilizará como comunicación principal con los servidores de los microservicios la comunicación gRPC, y en caso de fallo con estos servidores, deberá utilizar la comunicación MOM para enviar la solicitud

## 1.1. Que se logro: 
Se diseñaron e implementaron correctamente todos los servicios y servidores propuestos, se utilizo una ip elastica para la entrada de solicitudes via HTTP segun fue solicitado. Todo el sistema gRPC y MOM funcionan al igual que el apiGateway.

## 1.2. Que falto: 
No fue posible implementar la repuesta del servidor #2 por fuera de la consola (En el apiGateway), de igual forma todo el sistema MOM funciona y el servidor 2 realiza las solicitudes.

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizo Flask para visualizar las respuestas del servidor utilizando HTTP, se crearon 4 servidores de AWS y se configuraron de la siguiente manera: Un servidor como apiGateway con IP elasica, un servidor que recibe solicitudes gRPC y las ejecute, un servidor corriendo RabbitMQ como servicio MOM, y un ultimo servidor que ejecuta las solicitudes encoladas en el MOM.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Debido a que todo el codigo esta escrito en python no es necesario compilar, sin embargo, el archivo .proto del gRPC si es necesario compilarlo para que funcione correctamente, esto se hace con el siguiente codigo:

sudo python3 -m grpc_tools.protoc -I ../protobufs --python_out=. --pyi_out=. --grpc_python_out=. ../protobufs/contrato.proto

Como librerias adicionales se utilizaron las siguientes:
- Flask: Carga y renderizado de las respuestas del servidor con .html. 
- os: Se utilizo para el manejo y busqueda de archivos en el servidor.
- grpc: Manejo de la mensajeria gRPC.
- pika: Manejo de RabbitMQ (Comunicacion MOM).

Como configuracion de las variables de ambiente se utilizaron los siguientes codigos:
-export hostip = 172.31.46.195
-export hostport = 8080
-export grpcipport = 172.31.38.44:50051
-export rabbithost=34.201.203.162
-export user=user
-export password=password

Como configuracion de directorios tenemos el siguiente arbol de directorios:

- reto2
   - apiGateway
       -protobufs
       -src ( En esta carpeta se encuentra el archivo para iniciar el server "apiGateway.py" )
          -templates
   - gRPC
      -protobufs
      -src ( En esta carpeta se encuentra el archivo para iniciar el server "gRPC.py" )
      -serverFiles
   - server2
      -src ( En esta carpeta se encuentra el archivo para iniciar el server "server2.py" )
      -serverFiles

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.
Se utilizaron las siguientes direcciones IP:

IP DE ENTRADA= 44.217.252.126 (Elastica)
IP de rabbithost= 34.201.203.162 (Elastica)

ip host privada = 172.31.46.195:8080
ip grppc privada = 172.31.38.44:50051


## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto

#### versión README.md -> 1.0 (2023-agosto)
