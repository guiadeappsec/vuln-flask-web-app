import urllib.request
from flask import render_template


def ssrf_page(request, app):
    return render_template(
        'ssrf.html'
    )


def ssrf_api(request, app):
    form = request.form

    name = form['name']
    email = form['email']
    original_picture_url = form['imageUrl']

    downloaded_url = _download_image(original_picture_url, app)

    return render_template(
        'ssrf.html',
        email=email,
        name=name,
        original_url=original_picture_url,
        profile_picture_url=downloaded_url
    )


def _download_image(url, app):
    if not url:
        return ''

    download_image_path = ''

    with urllib.request.urlopen(url) as f:
        download_image_path = f"{app.config['PUBLIC_UPLOAD_FOLDER']}/downloaded-image.png"

        with open(download_image_path, 'wb') as file:
            file_content = f.read()
            file.write(file_content)
            file.close()

    public_url = f"{app.config['PUBLIC_UPLOADS_URL']}/downloaded-image.png"

    return public_url