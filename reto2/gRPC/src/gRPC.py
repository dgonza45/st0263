import grpc
import os
from concurrent import futures
import contrato_pb2
import contrato_pb2_grpc
from google.protobuf.empty_pb2 import Empty


class FileListServicer(contrato_pb2_grpc.FileListServicer):
    def ListFiles(self, request, context):
        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles')  # Server files es la carpeta donde esta todo el contenido "multimedia" del server
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        response = contrato_pb2.FileResponse(files_found="\n".join(files))
        return response

class FindFileServicer(contrato_pb2_grpc.FindFileServicer):
    def FindFiles(self, request, context):
        search_files = request.files
        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serverFiles') # Server files es la carpeta donde esta todo el contenido "multimedia" del server
        files_found = [f for f in os.listdir(folder_path) if f.lower() in search_files and os.path.isfile(os.path.join(folder_path, f))]
        response = contrato_pb2.FileResponse(files_found="\n".join(files_found))
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    contrato_pb2_grpc.add_FileListServicer_to_server(FileListServicer(), server)
    contrato_pb2_grpc.add_FindFileServicer_to_server(FindFileServicer(), server)
    server.add_insecure_port(os.environ['grpcipport'])    # Ip y cosas importantes como variables de entorno.
    print("Server started")
    server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()




