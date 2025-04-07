import firebase_admin
from firebase_admin import credentials, storage, firestore
from secrets.firebase_values import STORAGE_BUCKET, DATABASE_URL
import json

def initialize_firebase():
    """
    The function `initialize_firebase` initializes a Firebase app with specified credentials and
    configuration settings.
    :return: The `initialize_firebase` function is returning a Firestore client and a Cloud Storage
    bucket.
    """
    cred = credentials.Certificate("../secrets/etl-pipeline-edcbb-firebase-adminsdk-fbsvc-3fc4d5669d.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': STORAGE_BUCKET,
        'databaseURL': DATABASE_URL
    })
    return firestore.client(), storage.bucket()