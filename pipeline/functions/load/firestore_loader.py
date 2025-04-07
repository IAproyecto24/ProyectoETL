from google.cloud import firestore
from utils.logger import log_error

def update_warehouse(event, context):
    """
    The function `update_warehouse` updates a warehouse database with information from a given event and
    context in a Firestore database.
    
    :param event: The `event` parameter in the `update_warehouse` function likely contains information
    about the event that triggered the function. It seems to be structured as a dictionary with nested
    fields. The specific structure of the `event` parameter would depend on the event that is being
    handled by this function
    :param context: The `context` parameter in the `update_warehouse` function is typically used to
    provide information about the current execution context of the function. In this case, it seems to
    be used to extract the resource path from the context to determine the collection being updated
    """
    db = firestore.client()
    doc_path = context.resource.split('/documents/')[1]
    collection = doc_path.split('/')[0]

    try:
        # Actualizar Tabla de Hechos
        fact_ref = db.collection("hechos").document()
        fact_data = {
            "origen": collection,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "metadata": doc_path,
            "crimen": event['value']['fields'].get('crimen', {})
        }
        fact_ref.set(fact_data)

        # Actualizar Dimensiones
        dim_time_ref = db.collection("dim_tiempo").document()
        dim_time_ref.set({
            "año": event['value']['fields'].get('AÑO', {}).get('integerValue'),
            "mes": event['value']['fields'].get('MES', {}).get('integerValue')
        })
        dim_location_ref = db.collection("dim_ubicacion").document()
        dim_location_ref.set({
            "departamento": event['value']['fields'].get('Departamento', {}),
            "municipio": event['value']['fields'].get('Municipio', {})
        })

    except Exception as e:
        log_error("LoadError", str(e), doc_path)