"""
Connecting to Firebase and managing Firestore Database
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'idyllic-kit-328813',
})

firestore_db = firestore.client()


def add_data(collection, document, raw_data, db=firestore_db):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(raw_data)


def get_all_data(collection, db=firestore_db):
    col = db.collection(collection)
    docs = col.stream()
    return docs.to_dict()
