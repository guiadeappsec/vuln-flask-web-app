## Setup

### Requisites

* ImageMagick: https://imagemagick.org/index.php
* Python 3.7+
* Docker (if want to run in a container)

### Running

#### Run in Docker

```sh
# building
docker build -t poc-sast-python-flask .

# running
docker run -it -p 5000:5000 --rm --name poc-sast-python-flask poc-sast-python-flask
```


#### Run Local

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sh run.sh
```


## Vulns

### Hardcoded Credentials and Keys

```py
# db_helper.py
self.host = '10.0.0.99'
self.port = 3306
self.user = 'MyDbUser'
self.password = 'M1DbPassword'
```

```py
# api_keys.py

GOOGLE_RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
```

```html
<!-- base.html -->
 <script>
    // var googleCaptchaKey = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI';
    // var googleCatpchaSecretKey = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe';

    var googleCaptchaKey = '{{ GOOGLE_RECAPTCHA_SITE_KEY }}';
    var googleCatpchaSecretKey = '{{ GOOGLE_RECAPTCHA_SECRET_KEY }}';

</script>
```


### SQL Injection

URL: http://localhost:5000/sql-injection

```py
# vulns/sqlinjection/sql_injection.py

username = form.get('username')
password = form.get('password')
password_hash = _hash_password(password)

sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password_hash}'"

db_result = app.db_helper.execute_read(sql)
```


### XSS

Reflected: http://localhost:5000/xss/reflected?search=

```html
<!--
    Reflected
    templates/xss-reflected.html line 11
-->

{{ request.args.get('search') }}
```

Stored: http://localhost:5000/xss/stored

```html
<!--
    Stored
    templates/xss-stored.html line 33
-->

{% for msg in messages %}
    <li>
        <td>{{ msg }}</td>
    </li>
{% endfor %}
```


### File Upload

URL: http://localhost:5000/file-upload

```py
# vulns/file_upload/file_upload.py

# Command Injection in filename;
# just submit a file with the name:
# & touch hacked.txt & 
os.system(f'convert {temp_upload_file_path} -resize 50% {resized_image_path}')
```

```py
# vulns/file_upload/file_upload.py

# Insecure file validation
# just submit a malicious file ended with %00.png to bypass ext validation.
def _validate_file(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ALLOWED_EXTENSIONS

```

### Insecure Crypto

URL: http://localhost:5000/insecure-crypto


```py
# vulns/insecure_crypto/insecure_crypto.py

hash_pass = hashlib.md5(password.encode())
hash_text = hash_pass.hexdigest()
```

### SSRF

URL: http://localhost:5000/ssr

```py
# how it works:
# - The user sends an url of an image.
# - The api downloads the url and save for future usage.
# - The web shows the downloaded image.

# how to exploit:
# the url could be an local file, like: file:/etc/passwd


# vulns/ssrf/ssrf.py
 with urllib.request.urlopen(url) as f:
    download_image_path = f"{app.config['PUBLIC_UPLOAD_FOLDER']}/downloaded-image.png"

    with open(download_image_path, 'wb') as file:
        file_content = f.read()
        file.write(file_content)
        file.close()

public_url = f"{app.config['PUBLIC_UPLOADS_URL']}/downloaded-image.png"
```

### Path Traversal

URL: http://localhost:5000/path-traversal

```py
# how it works:
# The image on page contain a filename as an parameter in url.
# - http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg

# how to exploit
# change the image name to any file, like: 
# http://localhost:5000/path-traversal-img?img=../../Dockerfile


# vulns/path_traversal/path_traversal.py

def path_traversal_image(request, app):
    image_path = f"{app.config['PUBLIC_IMG_FOLDER']}/{request.args.get('img')}"

    return send_file(image_path)
```