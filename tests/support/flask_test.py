from unittest import TestCase, skip
from flask import Flask
import requests
from threading import Thread
from urllib.parse import parse_qs, urlparse
from wsgiref.simple_server import make_server
from .._vcr import vcr
from pw2client.support.flask import authorization_required, oauth


class FlaskSupportTest(TestCase):

    @classmethod
    def setUpClass(cls):
        httpd = cls.httpd = make_server('localhost', 3030, app)
        thr = cls._thr = Thread(target=httpd.serve_forever)
        thr.daemon = True
        thr.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls._thr.join()

    @vcr.use_cassette('present-access-grant-request.yaml')
    def test_redirect_to_authorization_url(self):
        res = requests.get('http://localhost:3030/')
        self.assertEqual(res.status_code, 200)
        history = [r.url for r in res.history]
        last_url = history[-1]
        self.assertListEqual(history, [
            'http://localhost:3030/',
            'http://localhost:3030/oauth/signin',
            last_url,
        ])
        last_url = urlparse(last_url)
        self.assertEqual(last_url.scheme, 'http')
        self.assertEqual(last_url.netloc, 'localhost:3000')
        self.assertEqual(last_url.path, '/oauth/authorize')
        self.assertEqual(parse_qs(last_url.query), {
            'response_type': ['code'],
            'client_id': ['QJDSMPTJWNFPZJ6WINEKJ2CZ5A'],
            'redirect_uri': ['http://localhost:3030/oauth/callback'],
            'scope':[ 'profile'],
        })
        self.assertEqual(res.url, 'http://localhost:3000/sign_in')

    @skip('TODO: test the flow')
    def test_the_rest_of_the_flow(self):
        raise NotImplementedError


#-------------------------------------------------------------------------------

app = Flask(__name__)
app.config.update(
    PW2_CLIENT_ID='QJDSMPTJWNFPZJ6WINEKJ2CZ5A',
    PW2_CLIENT_SECRET='O4EAKLNC6VHDJJZMXJ4TXC4GFA',
    SECRET_KEY=b'qhfuR/NGtD4hVm9n',
    TESTING=True,
)
app.register_blueprint(oauth, url_prefix='/oauth')

@app.route('/')
@authorization_required
def index(access_token):
    return 'OK'

@app.route('/discard')
@authorization_required
def discarded_token():
    return 'OK'
