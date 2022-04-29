from flask import Flask, render_template, request, redirect, url_for
from vulns.sql_injection.sql_injection_login import sql_injection_login_page, sql_injection_login_api
from vulns.sql_injection.sql_injection_search import sql_injection_search_page
from vulns.file_upload.file_upload import file_upload_page, file_upload_api
from vulns.xssinjection.xss_reflected import xss_reflected_page
from vulns.xssinjection.xss_stored import xss_stored_page, xss_stored_api
from vulns.ssrf.ssrf import ssrf_page, ssrf_api
from vulns.path_traversal.path_traversal import path_traversal_page, path_traversal_image
from vulns.idor.idor import idor_login_page, idor_login_api, idor_profile_page
from vulns.iframe_injection.iframe_injection import iframe_injection_page
from util import get_root_dir
from db_helper import db_helper
from db_models import db_models
from middlewares import require_api_key


app = Flask(__name__)

app.config['TEMP_UPLOAD_FOLDER'] = f"{get_root_dir()}/temp/uploads"
app.config['PUBLIC_UPLOAD_FOLDER'] = f"{get_root_dir()}/static/uploads"
app.config['PUBLIC_IMG_FOLDER'] = f"{get_root_dir()}/static/img"
app.config['STATIC_BASE_URL'] = '/static'
app.config['PUBLIC_UPLOADS_URL'] = f"{app.config['STATIC_BASE_URL']}/uploads"


db_helper.initialize()
app.db_helper = db_helper
app.db_models = db_models

@app.before_request
@require_api_key
def before_request():
    pass


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/reset-database', methods=['POST'])
def reset_database():
    db_helper.reset_database()
    return redirect(url_for('home', reset_db=1))


@app.route('/sql-injection/login', methods=['GET', 'POST'])
def sql_injection_login():
    if request.method == 'GET':
        return sql_injection_login_page(request, app)

    return sql_injection_login_api(request, app)


@app.route('/sql-injection/search', methods=['GET'])
def sql_injection_search():
    return sql_injection_search_page(request, app)


@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        return file_upload_api(request, app)
    
    return file_upload_page()
    

@app.route('/xss/reflected', methods=['GET'])
def xss_reflected():
    return xss_reflected_page(request, app)


@app.route('/xss/stored', methods=['GET', 'POST'])
def xss_stored():
    if request.method == 'GET':
        return xss_stored_page(request, app)

    return xss_stored_api(request, app)


@app.route('/ssrf', methods=['GET', 'POST'])
def ssrf():
    if request.method == 'GET':
        return ssrf_page(request, app)

    return ssrf_api(request, app)


@app.route('/path-traversal', methods=['GET'])
def path_traversal():
    return path_traversal_page(request, app)


@app.route('/path-traversal-img', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)


@app.route('/idor/login', methods=['GET', 'POST'])
def idor_login():
    if request.method == 'GET':
        return idor_login_page(request, app)

    return idor_login_api(request, app)


@app.route('/idor/profile', methods=['GET'])
def idor_profile():
    return idor_profile_page(request, app)


@app.route('/iframe-injection', methods=['GET'])
def iframe_injection():
    return iframe_injection_page(request, app)