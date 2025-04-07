import pandas as pd
from google.cloud import storage
from utils.logger import log_error

def extract_data(event, context):
    """
    The `extract_data` function extracts data from an Excel file stored in a cloud storage bucket,
    processes it, and saves the cleaned data as a CSV file back to the bucket.
    
    :param event: The `event` parameter in the `extract_data` function likely contains information about
    the file being processed. It seems to be a dictionary with keys such as 'name' and 'bucket' that
    provide details about the file path and bucket name where the file is located. This function appears
    to be designed
    :param context: The `context` parameter in the `extract_data` function typically provides
    information about the execution environment and the context in which the function is running. It can
    include details such as the function name, the Cloud Function version, the event type, and other
    relevant metadata
    :return: If the file path does not contain "raw/policia" or "raw/fiscalia", an error message is
    logged and the function returns without further processing. If an exception occurs during the file
    processing (downloading, reading, cleaning, and uploading), an error message with the exception
    details is logged.
    """
    file = event
    file_path = file['name']
    bucket_name = file['bucket']

    # Identificar origen (policia/fiscalia)
    if "raw/policia" in file_path:
        source = "policia"
    elif "raw/fiscalia" in file_path:
        source = "fiscalia"
    else:
        log_error("ExtractError", "Ruta no válida", file_path)
        return

    # Descargar y leer archivo
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    temp_file = "/tmp/temp_file"
    blob.download_to_filename(temp_file)

    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(temp_file, engine="openpyxl")
        elif file_path.endswith(".xls"):
            df = pd.read_excel(temp_file)
        else:
            log_error("ExtractError", "Formato no soportado", file_path)
            return

        # Eliminar nulos y guardar CSV
        df.dropna(inplace=True)
        output_path = file_path.replace("raw/", "extracted/").replace(".xlsx", ".csv").replace(".xls", ".csv")
        df.to_csv(f"/tmp/{output_path.split('/')[-1]}", index=False)

        # Subir CSV al bucket
        blob = bucket.blob(output_path)
        blob.upload_from_filename(f"/tmp/{output_path.split('/')[-1]}")

    except Exception as e:
        log_error("ExtractError", str(e), file_path)