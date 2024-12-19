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
CARPETA_S3 = 'Checklist/'  

# Carpeta local donde deseas guardar las imágenes
LOCAL_DIR = r'E:\media\img'

if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

def descargar_imagenes_s3(bucket_name, carpeta_s3, local_dir):
    # Listar objetos en el bucket con el prefijo (simula la carpeta)
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta_s3)
    
    if 'Contents' in response:
        # Iterar sobre los objetos en la carpeta especificada
        for obj in response['Contents']:
            file_name = obj['Key']
            local_path = os.path.join(local_dir, file_name.replace(carpeta_s3, ""))  # Eliminar el prefijo de la ruta

            # Crear subdirectorios si no existen
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Descargar el archivo solo si no existe localmente
            if not os.path.exists(local_path):
                print(f"Descargando {file_name}...")
                s3.download_file(bucket_name, file_name, local_path)
            else:
                print(f"{file_name} ya existe, saltando descarga.")
    else:
        print(f"No se encontraron objetos en la carpeta {carpeta_s3} del bucket {bucket_name}.")

    print("Descarga completada.")

# Llamar a la función para descargar la carpeta específica
descargar_imagenes_s3(BUCKET_NAME, CARPETA_S3, LOCAL_DIR)
