# id-genie-django-sdk

Django SDK allows you to integrate MFA service provided by IDGenie in a few lines of code. After installing this SDK in your Django app, you would need to only add the following constants in your `settings.py`.

1. Add `idgenie_django` in your projects `INSTALLED_APPS`.
```py
INSTALLED_APPS = [
    ...,
     
    'idgenie_django',
]
```

2. Add the following middleware. Make sure that IDGenie middleware is added after `django.contrib.auth.middleware.AuthenticationMiddleware`
```py
MIDDLEWARE = [
    ...,
    'idgenie_django.middleware.IDGenieMFAMiddleware',
    ...
]
```

3. Grab you `secret` key, and add the following constants as well (these are provided in your configurations tab at app.idgenie.de):
```py
ID_GENIE_SESSION_ENDPOINT,
ID_GENIE_RP_NAME,
ID_GENIE_SESSION_ENDPOINT_MFA_PUSH,
ID_GENIE_VALIDATION_URL,

CLIENT_SECRET = <your secret goes here>
```

4. Lastly, add the urls provided by `idgenie_django`, by importing them in you apps main `urls.py`.

Voila! and you are done. You can also consult our demo Django app [here](https://github.com/ID-Genie/django-demo-app). 
