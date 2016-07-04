from app.app import app
import os

port = int(os.getenv("PORT"))

app.run(host='0.0.0.0', port=port)
