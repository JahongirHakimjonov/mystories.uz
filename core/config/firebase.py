import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("assets/mystories.json")
firebase_admin.initialize_app(cred)
