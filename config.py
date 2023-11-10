from dotenv import load_dotenv  # Instalar con pip install python-dotenv
import firebase_admin
load_dotenv()  # Carga todo el contenido de .env en variables de entorno


class Config:
    SERVER_NAME = "localhost:5050"
    DEBUG = True
    firebase_admin.initialize_app()
