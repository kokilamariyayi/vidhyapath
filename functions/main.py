import sys
import os

# Add the parent directory to sys.path so we can import the backend package
# Firebase Functions Gen 2 expects dependencies in a specific way
# We add the root directory to path to find "backend"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from firebase_functions import https_fn
from backend.main import app
from mangum import Mangum

# Bridge FastAPI to Cloud Functions using Mangum
handler = Mangum(app, lifespan="off")

@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    # Firebase Functions on_request handles the routing
    # We can use mangum to process the request
    return https_fn.Response("VidyaPath Backend is active. Connect to /chat or /translate.")
