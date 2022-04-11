from waitress import serve

from app import app

serve(app, listen='*:5000')