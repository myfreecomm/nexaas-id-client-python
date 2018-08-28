from unittest import TestCase
from datetime import date
from requests.exceptions import HTTPError
from urllib.parse import parse_qs, urlparse
from uuid import UUID
from ._vcr import vcr
from nexaas_id_client import NexaasIDClient, NexaasIDOAuthClient


class TestNexaasIDClient(TestCase):
    @staticmethod
    def build_oauth_client():
        return NexaasIDOAuthClient(
            'E4KAAPDCBBBZVHZBTXZX6EEBDU',
            'F6K34MJSAZBC7FNG7XBBS6HMRY',
            redirect_uri='http://localhost:9000/callback',
        )

    @classmethod
    def build_api_client(cls):
        return NexaasIDClient.from_oauth(
            '35822300c02a679292f2dda5069aa4a997419dc114637dc8aae62f55394a52b0',
            client=cls.build_oauth_client(),
        )

    def test_tuple_attributes(self):
        client = self.build_api_client()
        self.assertEqual(
            client.access_token,
            '35822300c02a679292f2dda5069aa4a997419dc114637dc8aae62f55394a52b0',
        )
        self.assertEqual(client.id, 'E4KAAPDCBBBZVHZBTXZX6EEBDU')
        self.assertEqual(client.secret, 'F6K34MJSAZBC7FNG7XBBS6HMRY')
        self.assertEqual(client.server.netloc, 'localhost:3000')
        self.assertEqual(client.server.path, '/')
        self.assertEqual(
            client.navbar_url,
            'http://localhost:3000/api/v1/widgets/navbar.js?'
            'access_token={}'.format(client.access_token),
        )
        self.assertEqual(
            client.user_widget_url,
            'http://localhost:3000/api/v1/widgets/user.js?'
            'access_token={}'.format(client.access_token),
        )

    @vcr.use_cassette('personal_info.yaml')
    def test_personal_info(self):
        client = self.build_api_client()
        info = client.personal_info
        self.assertEqual(info.id, UUID('9680f8e1-ff10-46b5-bedb-f4545adabfca'))
        self.assertEqual(info.full_name, 'Rodrigo Cacilhas')
        self.assertEqual(info.first_name, 'Rodrigo')
        self.assertEqual(info.last_name, 'Cacilhas')
        self.assertEqual(info.nickname, 'cacilhas')
        self.assertEqual(info.email, 'rodrigo.cacilhas@nexaas.com')
        self.assertEqual(info.birth, date(1975, 11, 20))
        self.assertEqual(info.gender, 'male')
        self.assertEqual(info.language, 'pt-br')
        self.assertEqual(
            info.picture,
            'http://localhost:3000/images/avatar/'
            '9680f8e1-ff10-46b5-bedb-f4545adabfca?size=140',
        )
        self.assertEqual(info.timezone, 'America/Sao_Paulo')
        self.assertEqual(info.country, 'BR')
        self.assertEqual(info.city, 'Niterói / RJ')

    @vcr.use_cassette('professional_info.yaml')
    def test_professional_info(self):
        client = self.build_api_client()
        info = client.professional_info
        self.assertEqual(info.id, UUID('9680f8e1-ff10-46b5-bedb-f4545adabfca'))
        self.assertEqual(info.profession, 'Desenvolvedor')
        self.assertEqual(info.company, 'NexaaS')
        self.assertEqual(info.position, 'Analista de Desenvolvimento Sênior I')

    @vcr.use_cassette('emails.yaml')
    def test_emails(self):
        client = self.build_api_client()
        info = client.emails
        self.assertEqual(info.id, UUID('9680f8e1-ff10-46b5-bedb-f4545adabfca'))
        self.assertListEqual(
            info.emails,
            ['rodrigo.cacilhas@nexaas.com', 'batalema@cacilhas.info'],
        )

    @vcr.use_cassette('contacts.yaml')
    def test_contacts(self):
        client = self.build_api_client()
        info = client.contacts
        self.assertEqual(info.id, UUID('9680f8e1-ff10-46b5-bedb-f4545adabfca'))
        self.assertListEqual(
            info.phone_numbers,
            ['+55-21-999999999'],
        )

    @vcr.use_cassette('invite.yaml')
    def test_invite(self):
        client = self.build_api_client()
        info = client.invite('blablabla@example.com')
        self.assertEqual(info.requester, UUID('9680f8e1-ff10-46b5-bedb-f4545adabfca'))
        self.assertEqual(info.email, 'blablabla@example.com')
        self.assertEqual(info.id, UUID('813500b4-ab60-41ce-a036-61563aec297d'))
