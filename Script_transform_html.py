import sys
import boto3
import csv
import tempfile
from datetime import date
from bs4 import BeautifulSoup

# Crea una conexión a S3
s3 = boto3.client('s3')

# Define la ruta del archivo HTML
ruta = 'raw/'

# Define la ruta del archivo CSV
ruta_csv = 'final/'

# Define el nombre del archivo como 'contenido_YYYY-MM-DD.html' usando la fecha actual
nombre_archivo = 'contenido_{}.html'.format(date.today().strftime("%Y-%m-%d"))

# Descarga el archivo HTML del bucket S3 y analízalo con BeautifulSoup
bucket_name = 'news5927'
key = ruta + nombre_archivo
response = s3.get_object(Bucket=bucket_name, Key=key)
html_bytes = response['Body'].read()
soup = BeautifulSoup(html_bytes, 'html.parser')

# Encuentra los elementos de artículo y extrae los atributos de datos
contenido = soup.find_all("article")

# Crea un archivo CSV temporal y escribe los resultados
with tempfile.TemporaryFile(mode='w+t') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')  # utilizar | como separador
    writer.writerow(['id', 'Categoria', 'Noticia'])
    count = 1
    for articulo in contenido:
        try:
            writer.writerow([count, articulo["data-category"], articulo["data-name"]])
            count += 1
        except:
            pass
    # Mueve el cursor al principio del archivo
    csvfile.seek(0)
    # Lee el contenido del archivo temporal
    csv_content = csvfile.read()

# Sube el archivo CSV a S3
nombre_archivo_csv = 'resultado_{}.csv'.format(date.today().strftime("%Y-%m-%d"))
key_csv = ruta_csv + date.today().strftime("year=%Y/month=%m/day=%d/") + nombre_archivo_csv
s3.put_object(Body=csv_content.encode('utf-8'), Bucket=bucket_name, Key=key_csv)