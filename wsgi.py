from service import app
from service.models import Product

if __name__ == "__main__":
    Product.init_db(app)
    
    app.run(host="0.0.0.0", port=8080)