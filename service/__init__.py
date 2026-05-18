"""
Service Package
"""
import os
from flask import Flask
from flask_talisman import Talisman

# Initialize Flask app
app = Flask(__name__)

# Intitialize Talisman for security headers
talisman = Talisman(app,
                    content_security_policy={
                        'default-src': '\'self\''
                    },
                    referrer_policy='no-referrer'
                    )

# Import the routes after the Flask app is created
from service import routes, models
from service.models import Account

# Define routes for internal health checking
@app.route('/health', methods=['GET'])
def health():
    """Service health check"""
    return {"status": "OK"}, 200

# Set up database
models.init_db(app)

app.logger.info("Service initialized")