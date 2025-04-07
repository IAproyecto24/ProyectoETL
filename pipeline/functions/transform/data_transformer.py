import pandas as pd
from datetime import datetime
from utils.logger import log_error
from google.cloud import storage
from google.cloud import firestore

def transform_data(event, context):
    """
    The `transform_data` function processes a CSV file stored in a cloud storage bucket, performs data
    transformations based on column names, and saves the transformed data into Firestore under specific
    collections based on the file path.
    
    :param event: The `event` parameter in the `transform_data` function likely contains information
    about the file being processed, such as its name and the bucket it belongs to. This information is
    used to determine the collection to which the transformed data will be saved in Firestore
    :param context: The `context` parameter in the `transform_data` function typically provides
    information about the execution environment and the event that triggered the function. It can
    include details such as the function name, resource information, and authentication details. In this
    specific function, the `context` parameter is not being used directly,
    :return: If the file path contains "extracted/policia" or "extracted/fiscalia", the data from the
    CSV file will be transformed and saved into Firestore under the respective collection ("policia" or
    "fiscalia"). If the file path does not match any of these patterns, an error will be logged and the
    function will return without further processing.
    """
    file = event
    file_path = file['name']
    bucket_name = file['bucket']

    if "extracted/policia" in file_path:
        collection = "policia"
    elif "extracted/fiscalia" in file_path:
        collection = "fiscalia"
    else:
        log_error("TransformError", "Ruta no válida", file_path)
        return

    # Descargar CSV
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    temp_file = "/tmp/temp.csv"
    blob.download_to_filename(temp_file)

    try:
        df = pd.read_csv(temp_file)

        # Transformaciones
        if 'CODIGO DANE' in df.columns:
            df['CODIGO DANE'] = df['CODIGO DANE'].astype(str)
        
        if 'FECHA HECHO' in df.columns:
            df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'])
            df['AÑO'] = df['FECHA HECHO'].dt.year
            df['MES'] = df['FECHA HECHO'].dt.month
        
        if 'TOTAL' in df.columns or 'CANTIDAD' in df.columns:
            numeric_col = 'TOTAL' if 'TOTAL' in df.columns else 'CANTIDAD'
            df[numeric_col] = pd.to_numeric(df[numeric_col], errors='coerce')
        
        if 'AÑOMESENTRADA' in df.columns:
            df[['AÑO', 'MES']] = df['AÑOMESENTRADA'].str.split('-', expand=True)
            df.drop('AÑOMESENTRADA', axis=1, inplace=True)

        # Guardar en Firestore
        db = firestore.client()
        for _, row in df.iterrows():
            doc_ref = db.collection(f"transformed/{collection}").document()
            doc_ref.set(row.to_dict())

    except Exception as e:
        log_error("TransformError", str(e), file_path)