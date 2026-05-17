import requests
from behave import given

@given('the following products')
def step_impl(context):
    """Delete all existing products and load new ones from Gherkin data table"""
    # 1. Ambil semua data lama
    res = requests.get(f"{context.base_url}/products")
    assert res.status_code == 200, f"Gagal mengambil data produk, status: {res.status_code}"
    
    # 2. Hapus satu per satu data lama agar database bersih
    for product in res.json():
        requests.delete(f"{context.base_url}/products/{product['id']}")
        
    # 3. Masukkan data baru dari tabel skenario BDD
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'].lower() in ['true', '1', 'yes'],
            "category": row['category']
        }
        res = requests.post(f"{context.base_url}/products", json=payload)
        # Tambahkan pesan di ujung assert agar kita tahu jika payload ditolak backend
        assert res.status_code == 201, f"Gagal memasukkan produk {row['name']}. Status: {res.status_code}, Respon: {res.text}"