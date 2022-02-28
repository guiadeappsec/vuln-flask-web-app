from flask import render_template
import hashlib


def insecure_crypto_page(request, app):
    return render_template('insecure-crypto.html')


def insecure_crypto_api(request, app):
    email = request.form['email']
    password = request.form['password']

    hash_pass = hashlib.md5(password.encode())
    hash_text = hash_pass.hexdigest()

    return {
        'email': email,
        'pass': password,
        'hash_pass': hash_text
    }
