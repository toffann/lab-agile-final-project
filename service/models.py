import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

# Ambil instansi db dari package service
from service import db

logger = logging.getLogger("flask.app")

class DataValidationError(Exception):
    """Digunakan untuk error validasi data yang tidak sesuai skema"""
    pass

class Category(Enum):
    """Enum untuk Kategori Produk"""
    UNKNOWN = 0
    CLOTHES = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5
    ELECTRONICS = 6  

class Product(db.Model):
    """Kelas Model untuk Tabel Product"""
    
    __tablename__ = "products"

    # Definisi Kolom Tabel Database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=Category.UNKNOWN.name
    )

    def create(self):
        """Membuat produk baru ke database"""
        logger.info("Creating %s", self.name)
        self.id = None  # id otomatis digenerate oleh database
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Memperbarui produk yang sudah ada"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called on a product with no ID")
        db.session.commit()

    def delete(self):
        """Menghapus produk dari database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Mengubah objek kelas menjadi bentuk Python Dictionary (untuk JSON)"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category.name  # Ambil string nama enum
        }

    def deserialize(self, data):
        """Membaca Python Dictionary untuk dimasukkan ke properti kelas"""
        try:
            self.name = data["name"]
            self.description = data.get("description", "")
            self.price = float(data["price"])
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError("Invalid type for boolean 'available'")
            self.category = getattr(Category, data["category"].upper(), Category.UNKNOWN)
        except KeyError as error:
            raise DataValidationError(f"Invalid Product: missing {error.args[0]}")
        except TypeError as error:
            raise DataValidationError(f"Invalid Product: body data error {error}")
        return self

    @classmethod
    def init_db(cls, app):
        """Inisialisasi database dari Flask App"""
        logger.info("Initializing database...")
        with app.app_context():
            db.create_all()  

    @classmethod
    def all(cls):
        """Mengambil semua rekaman data produk"""
        logger.info("Listing all products...")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Mencari produk berdasarkan ID"""
        logger.info("Finding product by id %s...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Mencari produk berdasarkan nama"""
        logger.info("Finding products by name %s...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """Mencari produk berdasarkan kategori"""
        logger.info("Finding products by category %s...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Mencari produk berdasarkan status ketersediaan"""
        logger.info("Finding products by availability %s...", available)
        return cls.query.filter(cls.available == available)