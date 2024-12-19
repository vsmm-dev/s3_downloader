import boto3
from dotenv import load_dotenv
import os

# Cargar las credenciales desde el archivo .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
BUCKET_NAME = os.getenv('AWS_BUCKET')

# Configurar el cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# Prefijo (carpeta) que deseas descargar
CARPETA_S3 = 'ImagenCliente/' 

# Carpeta local donde deseas guardar las imágenes
LOCAL_DIR = r'E:\media\img\Prooder_s3'

if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

def descargar_imagenes_s3(bucket_name, carpeta_s3, local_dir):
    # Inicializar un marcador para la paginación
    continuation_token = None
    
    while True:
        # Listar objetos en el bucket con el prefijo (simula la carpeta)
        if continuation_token:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=carpeta_s3,
                ContinuationToken=continuation_token
            )
        else:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta_s3)

        if 'Contents' in response:
            # Iterar sobre los objetos en la carpeta especificada
            for obj in response['Contents']:
                file_name = obj['Key']
                
                # Filtrar solo los objetos que están en las subcarpetas dentro de 'Checklist/'
                if file_name.startswith(carpeta_s3):  # Confirmar que está dentro del prefijo
                    local_path = os.path.join(local_dir, file_name)  # Usar la ruta completa del archivo

                    # Crear la estructura de carpetas si no existe
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    # Descargar solo si el archivo no existe en el destino
                    if not os.path.exists(local_path):
                        print(f"Descargando {file_name}...")
                        s3.download_file(bucket_name, file_name, local_path)
                    else:
                        print(f"{file_name} ya existe, saltando descarga.")
        
        # Si hay más objetos, paginar
        if response.get('IsTruncated'):  # Si hay más páginas
            continuation_token = response['NextContinuationToken']
        else:
            break  # No hay más objetos

    print("Descarga completada.")

# Llamar a la función para descargar la carpeta específica
descargar_imagenes_s3(BUCKET_NAME, CARPETA_S3, LOCAL_DIR)