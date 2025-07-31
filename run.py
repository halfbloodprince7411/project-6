from app import create_app
from flask_talisman import Talisman
import os

app = create_app()

# Only enforce HTTPS in production
if os.getenv("AZURE_ENV") == "PRODUCTION":
    Talisman(app, force_https=True, content_security_policy=None)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
