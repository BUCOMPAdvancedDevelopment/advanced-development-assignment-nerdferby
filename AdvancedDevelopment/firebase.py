"""
Connecting to Firebase and managing Firestore Database
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth as firebase_auth

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'idyllic-kit-328813',
})


class FirebaseClient:
    """Source: https://github.com/saadmk11/django-todo"""

    def __init__(self, collection):
        self._db = firestore.client()
        self._collection = self._db.collection(str(collection))

    def create(self, data, document: str = None):
        """Create item in firestore database"""
        doc_ref = self._collection.document(document)
        doc_ref.set(data)

    def update(self, document, data):
        """Update item on firestore database using document id"""
        doc_ref = self._collection.document(document)
        doc_ref.update(data)

    def delete_by_id(self, document):
        """Delete item on firestore database using document id"""
        self._collection.document(document).delete()

    def get_by_id(self, document):
        """Get item on firestore database using document id"""
        doc_ref = self._collection.document(document)
        doc = doc_ref.get()

        if doc.exists:
            return {**doc.to_dict(), "id": doc.id}
        return False

    def all(self):
        """Get all item from firestore database"""
        docs = self._collection.stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    def filter(self, field, condition, value):
        """Filter item using conditions on firestore database"""
        docs = self._collection.where(field, condition, value).stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]


class FirebaseAuth:
    def create_user(self, email, password):
        return firebase_auth.create_user(email=email, password=password)
