import datetime
import boto3

# URL de la página web a descargar
url = "https://www.eltiempo.com/"  

fecha_actual = datetime.date.today().strftime("%Y-%m-%d")  # Fecha actual en formato YYYY-MM-DD
nombre_archivo = f"contenido_{fecha_actual}.html"  # Nombre personalizado del archivo

# Descargar la página web y guardarla en un archivo local
try:
    urllib.request.urlretrieve(url, nombre_archivo)
    print("La página web se ha descargado exitosamente como", nombre_archivo)
except Exception as e:
    print("Ocurrió un error al descargar la página web:", e)

# Cargar el archivo en un bucket de S3
try:
    # Nombre del bucket y ruta del archivo en S3
    bucket = 'news5927'
    ruta_en_s3 = 'raw/' + nombre_archivo

    # Crear un cliente de S3
    s3 = boto3.client('s3')

    # Cargar el archivo en S3
    with open(nombre_archivo, 'rb') as f:
        s3.upload_fileobj(f, bucket, ruta_en_s3)

    print("El archivo se ha cargado en S3 con éxito en la ruta", ruta_en_s3)

except Exception as e:
    print("Ocurrió un error al cargar el archivo en S3:", e)