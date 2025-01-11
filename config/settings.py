import configparser
import os

# Pfad zur secrets.ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_FILE = os.path.join(BASE_DIR, "secrets.ini")

# INI-Datei laden
config = configparser.ConfigParser()
config.read(SECRETS_FILE)

# Werte auslesen
try:
    db_config = config["database"]
    DATABASE_URL = db_config["DATABASE_URL"]
    DATABASE_USER = db_config["DATABASE_USER"]
    DATABASE_NAME = db_config["DATABASE_NAME"]
    DATABASE_PORT = db_config["DATABASE_PORT"]
    DATABASE_PASSWORD = db_config["DATABASE_PASSWORD"]
except KeyError as e:
    raise RuntimeError(f"Fehlender Konfigurationswert: {e}")

# Verbindungs-String erstellen
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}"
)

class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
