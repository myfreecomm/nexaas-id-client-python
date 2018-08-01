# PW2 Client

This is a client for PassaporteWeb v.2. It brings support for generic OAuth
authentication and for Django and Flask frameworks.

## OAuth

The general use is:

```python
from pw2client import PW2OAuthClient

client = PW2OAuthClient(
    application_token,
    application_secret,
    server='v2.passaporteweb.com.br',
    redirect_uri=application_callback,
)
```

The authorization URL can get from `client.authorize_url` and the access token
can be retrieve in the callback procedure from `client.get_access_token(code)`,
where `code` is the access grant code.

### Settings for Django and Flask

- `PW2_CLIENT_ID`: the application token
- `PW2_CLIENT_SECRET`: the application secret
- `PW2_HOST`: the PassaporteWeb host
- `PW2_CLIENT_SCOPE`: the scope (can be None)

### Django

In Django you must include the following path to the main `urlpatterns`:

```python
    path('oauth/', include('pw2client.support.django.urls'))
```

The views that requires authorized access must be decorated:

```python
from pw2client.support.django.decorators import authorization_required

@authorization_required
def index(request, access_token):
    ...
```

If The view signature presents the `access_token` argument, the access token
will be supplied. Anyway you can retrieve de access token from the session,
under the key `oauth_access_token`.

It’s recommended offer a sign out view:

```python
from django.shortcuts import redirect

def signout(request):
    session = request.session
    if 'oauth_access_token' in session:
        del session['oauth_access_token']
    return redirect('index')
```

### Flask

The Flask support supply a blueprint capable of deal with PW2 OAuth.

The use:

```python
from flask import Flask
from pw2client.support.flask import oauth


app = Flask(__name__)
app.register_blueprint(oauth, url_prefix='/oauth')
```

The decorator is similar to Django support:

```python
from pw2client.support.flask import authorization_required, oauth
...

@app.route('/')
@authorization_required
def index(access_token):
    ...
```

If The view signature presents the `access_token` argument, the access token
will be supplied. Anyway you can retrieve de access token from the session,
under the key `oauth_access_token`.

It’s recommended offer a sign out view:

```python
from flask import redirect, session, url_for

@app.route('/signout')
def signout():
    if 'oauth_access_token' in session:
        del session['oauth_access_token']
    return redirect(url_for('index')
```

## TODO

- Sign out view for Django and Flask
- API access
