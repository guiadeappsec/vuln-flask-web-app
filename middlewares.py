import os
from functools import wraps
from flask import request, redirect, url_for, render_template_string


API_KEY = os.environ.get('VULN_FLASK_APP_API_KEY')

# Decorator to check if user is logged in
def require_api_key(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        api_key = request.cookies.get('api_key')
        if API_KEY is None or api_key == API_KEY:
            return f(*args, **kwargs)
        else:
            return render_template_string('no api key found'), 401
    return wrap
