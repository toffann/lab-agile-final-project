import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inisialisasi Aplikasi Flask
app = Flask(__name__)

# Konfigurasi Database standar (menggunakan SQLite untuk lokal)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../development.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-agile-key"

# Inisialisasi SQLAlchemy Ekstensi
db = SQLAlchemy(app)

# Atur Logging tingkat info untuk pelacakan REST API
app.logger.setLevel(logging.INFO)
app.logger.info("Initializing Product Service...")

# Import routes dan models di paling bawah untuk menghindari circular import
from service import routes, models