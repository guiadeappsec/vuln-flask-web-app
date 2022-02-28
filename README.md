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


