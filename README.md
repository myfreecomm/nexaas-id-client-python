# PW2 Client

This is a client for PassaporteWeb v.2. It brings support for generic OAuth
authentication and for Django and Flask frameworks.

## OAuth client

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
- `PW2_CLIENT_SCOPE`: the scope (can be `None`)

### Django

In Django you must include the following path to the main `urlpatterns`:

```python
    path('oauth/', include('pw2client.support.django.urls'))
```

The views that requires authorized access must be decorated:

```python
from pw2client import PW2Client
from pw2client.support.django.decorators import authorization_required

@authorization_required
def index(request, api_client: PW2Client):
    ...
```

Your view must expect an `api_client` as argument – see bellow. Anyway you can
retrieve de access token from the session, under the key `oauth_access_token`.

In order to logout, use the app route `signout`. The query string key
`next_url` inform where to redirect after sign out.

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
from pw2client import PW2Client
from pw2client.support.flask import authorization_required, oauth
...

@app.route('/')
@authorization_required
def index(api_client: PW2Client):
    ...
```

Your view must expect an `api_client` as argument – see bellow. Anyway you can
retrieve de access token from the session, under the key `oauth_access_token`.

In order to logout, use the blueprint route `signout`. The query string key
`next_url` inform where to redirect after sign out.

## API client

The API client is resposible for dealing with PW2 API.

You can get it this way:

```python
api_client = PW2Client.from_oauth(
    client.get_access_token(code),
    client=client,
)
```

Where `client` is the OAuth client and `code` is the access grant code.

But, if you are using a framework support, you don’t need to do it: views
decorated by `authorization_required` will receive an API client ready to use.

### Resource API

The API client attributes:

- `access_token: str` - the access token
- `id: str` – the client id
- `secret: str` – the client secret
- `server: urllib.parse.ParseResult` – the PW2 server
- `personal_info: PersonalInfo` – the user’s personal data
- `professional_info: ProfessionalInfo` – the user’s professional data
- `emails: Emails` – a dictionary containing user id and the its e-mails list
- `contacts: Contacts` – a dictionary containing user id and its phone numbers
  and eventually other contacts
- `invite(email: str) -> Invitation` – invite another user to the current
  application

The classes `PersonalInfo`, `ProfessionalInfo`, `Emails`, `Contacts` and
`Invitation` are built on demand metaprogrammatically, and have an `id`
attribute (`uuid.UUID`) at least.

Other attributes you may expect:

- `PersonalInfo`
    - `name: str`
    - `nickname: str`
    - `email: str`
    - `birth: datetime.date`
    - `gender: str`
    - `language: str`
    - `picture: str`
    - `timezone: str`
    - `country: str`
    - `city: str`
    - `bio: str`

- `ProfessionalInfo`
    - `profession: str`
    - `company: str`
    - `position: str`

- `Emails`
    - `emails: List[str]`

- `Contacts`:
    - `phone_numbers: List[str]`

- `Invitation`:
    - `email` (invited user)
    - `requester` (inviter id)
