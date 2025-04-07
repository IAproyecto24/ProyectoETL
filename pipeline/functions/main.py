from firebase_functions import storage_fn, firestore_fn
from extract.police_fiscalia_extractor import extract_data
from transform.data_transformer import transform_data
from load.firestore_loader import update_warehouse

"""
    The function `on_raw_file_upload` is triggered when an object is finalized in storage and calls the
    `extract_data` function with the event data.
    
    :param event: The `event` parameter is an object of type `storage_fn.CloudEvent`, which represents
    an event related to file upload in a cloud storage system
    :type event: storage_fn.CloudEvent
"""
@storage_fn.on_object_finalized()
def on_raw_file_upload(event: storage_fn.CloudEvent):
    extract_data(event, None)


"""
    The function `on_extracted_file_upload` is triggered when an object is finalized in storage and
    calls the `transform_data` function with the event data.
    
    :param event: The `event` parameter is of type `storage_fn.CloudEvent`, which represents an event
    related to object finalization in a storage system. This event is triggered when a file has been
    finalized or uploaded to the storage system
    :type event: storage_fn.CloudEvent
"""
@storage_fn.on_object_finalized()
def on_extracted_file_upload(event: storage_fn.CloudEvent):
    transform_data(event, None)

"""
    This Python function triggers an update to a warehouse when a document is created in a Firestore
    collection.
    
    :param event: The `event` parameter in the `on_transformed_doc_create` function is an object that
    contains information about the event that triggered the function. This information typically
    includes details about the document that was created or updated, such as its data, path, and
    metadata. You can use this `event`
    :type event: firestore_fn.Event
"""
@firestore_fn.on_document_created(document="transformed/{collection}/{docId}")
def on_transformed_doc_create(event: firestore_fn.Event):
    update_warehouse(event, None)
