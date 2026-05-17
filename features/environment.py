import os
from selenium import webdriver

# Membaca konfigurasi URL tujuan, jika lokal arahkan ke port server Flask kita (8080)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

def before_all(context):
    """Dijalankan sekali sebelum semua pengujian dimulai"""
    # Menyiapkan variabel global base_url agar bisa dipanggil di load_steps.py
    context.base_url = BASE_URL
    
    # Inisialisasi Selenium Headless Chrome Driver (biar tes berjalan di latar belakang)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    context.driver = webdriver.Chrome(options=options)

def after_all(context):
    """Dijalankan sekali setelah semua pengujian selesai"""
    # Menutup browser otomatis setelah tes beres
    context.driver.quit()