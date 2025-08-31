import requests
import time


class StackspotAuth:
    def __init__(self, client_id, client_secret, realm):
        self._client_id = client_id
        self._client_secret = client_secret
        self._realm = realm
        self._auth_response = None
        self._at = None

    def _fetch_token(self):
        res = requests.post(
            url=f'https://idm.stackspot.com/{self._realm}/oidc/oauth/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret
            }
        )
        if res.status_code != 200:
            raise Exception(f'{res.status_code} - Error authenticating on Stackspot: {res.text}')
        return res.json()

    def get_access_token(self):
        if (self._auth_response is None or self._auth_response['access_token']
                or ((self._at + self._auth_response['expires_in']) <= time.time())):
            self._auth_response = self._fetch_token()
            self._at = time.time()
        return self._auth_response['access_token']
