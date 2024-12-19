import boto3
import os

# Configurar el cliente de S3
s3 = boto3.client('s3')

BUCKET_NAME = 'tu-nombre-de-bucket' 
LOCAL_DIR = './img'

# Crear la carpeta local si no existe
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

# Función para descargar imágenes desde S3
def descargar_imagenes_s3(bucket_name, local_dir):
    # Listar objetos en el bucket S3
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        # Recorrer todos los objetos en el bucket
        for obj in response['Contents']:
            file_name = obj['Key']
            local_path = os.path.join(local_dir, file_name)
            
            # Crear subdirectorios si no existen
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Descargar el archivo solo si no existe localmente
            if not os.path.exists(local_path):
                print(f"Descargando {file_name}...")
                s3.download_file(bucket_name, file_name, local_path)
            else:
                print(f"{file_name} ya existe, saltando descarga.")
    else:
        print(f"No se encontraron objetos en el bucket {bucket_name}.")

    print("Descarga completada.")

# Ejecutar la función para descargar las imágenes
descargar_imagenes_s3(BUCKET_NAME, LOCAL_DIR)
