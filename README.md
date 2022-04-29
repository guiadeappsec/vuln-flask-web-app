## Setup

### Requisites

* ImageMagick: https://imagemagick.org/index.php
* Python 3.7+
* Docker (if want to run in a container)


### Running

#### Run in Docker

```sh
# building
docker build -t vuln-flask-web-app .

# running
docker run -it -p 5000:5000 --rm --name vuln-flask-web-app vuln-flask-web-app
```


#### Run Local

```
python3 -m venv venv
source venv/bin/activate
sh setup.sh
sh run.sh
```


### Options
#### Restricting Access (optional)

By default, the api key is set to `None` and any request will be allowed.

If you want to restrict the access to the app, just set the environment variable named `VULN_FLASK_APP_API_KEY` with your secret:

```sh
export VULN_FLASK_APP_API_KEY=myapisecret
```

Now, every request should include a cookie named `api_key` with the value of the `VULN_FLASK_APP_API_KEY` environment variable.

```http
GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Host: localhost:5000
...

Cookie: api_key=myapisecret

...
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

URL: http://localhost:5000/sql-injection/login

```py
# vulns/sql_injection/sql_injection_login.py

username = form.get('username')
password = form.get('password')
password_hash = _hash_password(password)

sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password_hash}'"

db_result = app.db_helper.execute_read(sql)
```

URL: http://localhost:5000/sql-injection/search

```py
# vulns/sql_injection/sql_injection_search.py

search = request.args.get('q')

sql = f"SELECT * FROM products WHERE name LIKE '%{search}%'"

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
command = f'convert "{temp_upload_file_path}" -resize 50% "{resized_image_path}"'
os.system(command)
```

```py
# vulns/file_upload/file_upload.py

# Insecure file validation
# just submit a malicious file ended with %00.png to bypass ext validation.
def _validate_file(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ALLOWED_EXTENSIONS

```

```py
# vulns/file_upload/file_upload.py

# It's possible to perform a LFI attack by submitting a file with a path that points to a file outside the web server's root directory.
# just submit a file with the name:
# ../../myfile.png
original_file_name = file.filename
temp_upload_file_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], original_file_name)
file.save(temp_upload_file_path)
```

### Insecure Crypto

```py
# vulns/sqlinjection/sql_injection.py

def _hash_password(password):
    md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
    return md5_pass
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


### IDOR

URL: http://localhost:5000/idor

```py
# how it works:
# The user can login at the http://localhost:5000/idor/login.
# It will set two cookies: user_id and session_token.
# After the login, the user will be redirected to http://localhost:5000/idor/profile.
# The profile page will check the cookies and if the user is logged in, it will show the user profile based on its user_id cookie.
# Try change the user_id cookie to any other user id and see what happens.

# vulns/idor/idor.py

user_id = request.cookies.get('user_id')

db_result = app.db_helper.execute_read(
    f"SELECT * FROM users WHERE id=:user_id",
    { 'user_id': user_id }
)

if len(db_result) == 0:
    return render_template('idor/idor_profile.html', user=None), 404

user = list(
    map(
        lambda u: app.db_models.UserDbModel(u),
        db_result
    )
)[0]

return render_template('idor/idor_profile.html', user=user)
```

### IFrame Injection

URL: http://localhost:5000/iframe-injection?page=/static/pages/about.html

```py
# The attacker could set the page arg to an evil url and share it with the victim.
# Just change the URL to: http://localhost:5000/iframe-injection?page=http://example.com

# vulns/iframe_injection/iframe_injection.py
def iframe_injection_page(request, app):
    iframe_url = request.args.get('page')
    return render_template("iframe_injection.html", iframe_url=iframe_url)
```

```html
{% extends "base.html" %}
{% block content %}
<h2>Iframe Injection</h2>

<iframe src="{{ iframe_url }}" frameborder="0"></iframe>

{% endblock %}
```