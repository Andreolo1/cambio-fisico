import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image
import streamlit as st

# Configuración de Google Drive
CREDENCIALES_JSON = "drive-key.json"  # Ruta al archivo JSON de credenciales
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CARPETA_DRIVE_ID = "14CXQsA8LrNjTcKDpowvcUgwJCW82fTMG"  # Reemplaza con el ID de tu carpeta en Drive

def conectar_google_drive():
    """Conecta a Google Drive y devuelve el servicio."""
    creds = service_account.Credentials.from_service_account_file(CREDENCIALES_JSON, scopes=SCOPES)
    servicio = build("drive", "v3", credentials=creds)
    return servicio

def obtener_ultima_imagen_drive():
    """
    Obtiene la última imagen de la carpeta en Google Drive.
    
    Returns:
        str: Ruta temporal de la imagen descargada.
    """
    try:
        # Conectar a Google Drive
        servicio = conectar_google_drive()
        
        # Listar archivos en la carpeta
        resultados = servicio.files().list(
            q=f"'{CARPETA_DRIVE_ID}' in parents",
            fields="files(id, name, createdTime)"
        ).execute()
        
        archivos = resultados.get("files", [])
        
        if not archivos:
            return None
        
        # Ordenar archivos por fecha de creación (el más reciente primero)
        archivos.sort(key=lambda x: x["createdTime"], reverse=True)
        
        # Obtener el ID del archivo más reciente
        ultimo_archivo = archivos[0]
        archivo_id = ultimo_archivo["id"]
        archivo_nombre = ultimo_archivo["name"]
        
        # Descargar la imagen
        request = servicio.files().get_media(fileId=archivo_id)
        fh = io.BytesIO()
        descargador = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = descargador.next_chunk()
        
        # Guardar la imagen temporalmente
        ruta_temporal = f"temp_{archivo_nombre}"
        with open(ruta_temporal, "wb") as f:
            f.write(fh.getvalue())
        
        return ruta_temporal
    except Exception as e:
        print(f"Error al obtener la imagen desde Google Drive: {e}")
        return None

def mostrar_imagen_desde_drive():
    """Muestra la última imagen de la carpeta en Google Drive."""
    ruta_imagen = obtener_ultima_imagen_drive()
    
    if ruta_imagen:
        st.image(ruta_imagen, caption="Última imagen registrada", use_column_width=True)
        os.remove(ruta_imagen)  # Eliminar la imagen temporal después de mostrarla
    else:
        st.warning("No se encontraron imágenes en la carpeta de Google Drive.")