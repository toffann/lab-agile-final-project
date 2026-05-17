import os
import sys
import logging
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service.utils import log_handlers

# Initialize Flask Application
app = Flask(__name__)
app.config.from_object("config")

# Initialize Application Security
talisman = Talisman(app, force_https=False)
CORS(app, resources={r"/*": {"origins": "*"}})

# Dependencies setup and logging routing
log_handlers.init_logging(app, "gunicorn.error")
app.logger.info("Service initialized successfully with Talisman and CORS headers security configuration.")

# Import routes after app initialization to avoid circular import issues
from service import routes, models