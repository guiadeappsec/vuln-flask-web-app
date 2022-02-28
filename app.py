from flask import Flask, render_template, request, redirect, url_for
from vulns.sqlinjection.sql_injection import sql_injection_page
from vulns.file_upload.file_upload import file_upload_page, file_upload_api
from vulns.xssinjection.xss_reflected import xss_reflected_page
from vulns.xssinjection.xss_stored import xss_stored_page, xss_stored_api
from vulns.insecure_crypto.insecure_crypto import insecure_crypto_api, insecure_crypto_page
from vulns.ssrf.ssrf import ssrf_page
from vulns.path_traversal.path_traversal import path_traversal_page, path_traversal_image
from util import get_root_dir
from db_helper import db_helper


app = Flask(__name__)

app.config['TEMP_UPLOAD_FOLDER'] = f"{get_root_dir()}/temp/uploads"
app.config['PUBLIC_UPLOAD_FOLDER'] = f"{get_root_dir()}/static/uploads"
app.config['PUBLIC_IMG_FOLDER'] = f"{get_root_dir()}/static/img"
app.config['STATIC_BASE_URL'] = '/static'
app.config['PUBLIC_UPLOADS_URL'] = f"{app.config['STATIC_BASE_URL']}/uploads"


db_helper.initialize()
app.db_helper = db_helper


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/reset-database', methods=['POST'])
def reset_database():
    db_helper.reset_database()
    return redirect(url_for('home', reset_db=1))


@app.route('/sql-injection')
def sql_injection():
    return sql_injection_page(request, app)


@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        return file_upload_api(request, app)
    
    return file_upload_page()
    

@app.route('/xss/reflected', methods=['GET'])
def xss_reflected():
    return xss_reflected_page(request)


@app.route('/xss/stored', methods=['GET', 'POST'])
def xss_stored():
    if request.method == 'GET':
        return xss_stored_page(request, app)

    return xss_stored_api(request, app)


@app.route('/insecure-crypto', methods=['GET', 'POST'])
def insecure_crypto():
    if request.method == 'GET':
        return insecure_crypto_page(request, app)

    return insecure_crypto_api(request, app)


@app.route('/ssrf', methods=['GET'])
def ssrf():
    return ssrf_page(request, app)


@app.route('/path-traversal', methods=['GET'])
def path_traversal():
    return path_traversal_page(request, app)


@app.route('/path-traversal-img', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)