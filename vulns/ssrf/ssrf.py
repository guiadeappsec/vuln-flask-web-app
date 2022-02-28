import urllib.request
from flask import render_template


def ssrf_page(request, app):
    profile_picture_url = request.args.get('profilePictureUrl')

    download_image_path = ''

    with urllib.request.urlopen(profile_picture_url) as f:
        download_image_path = f"{app.config['PUBLIC_UPLOAD_FOLDER']}/downloaded-image.png"

        with open(download_image_path, 'wb') as file:
            file_content = f.read()
            file.write(file_content)
            file.close()

    public_url = f"{app.config['PUBLIC_UPLOADS_URL']}/downloaded-image.png"

    return render_template(
        'ssrf.html',
        profile_picture_url=public_url
    )

