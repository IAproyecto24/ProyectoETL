from datetime import datetime
from firebase_admin import firestore

db = firestore.client()

def log_error(error_type, message, file_path=None):
    """
    The function `log_error` logs an error message along with its type, timestamp, and optional file
    path to a database collection.
    
    :param error_type: The `error_type` parameter in the `log_error` function is used to specify the
    type or category of the error that occurred. It could be a string indicating the nature of the
    error, such as "Runtime Error", "Syntax Error", "Database Error", etc
    :param message: The `message` parameter in the `log_error` function is a string that represents the
    error message or description that you want to log. It provides information about the error that
    occurred, helping in debugging and troubleshooting issues in the application
    :param file_path: The `file_path` parameter in the `log_error` function is an optional parameter
    that represents the path to the file where the error occurred. If provided, it will be included in
    the log entry along with the error type and message. If not provided, the `file_path` will default
    to
    """
    log_ref = db.collection("logs").document()
    log_ref.set({
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "message": message,
        "file": file_path
    })