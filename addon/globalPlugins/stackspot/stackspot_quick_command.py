import time
import requests
from json import dumps
from datetime import  datetime, timedelta


class StackspotQuickCommand:

    def __init__(self, token):
        self._id = None
        self._token = token

    def quick_command(self):
        return self

    def execute(self, slug, upload_ids):
        res = requests.post(
            url=f'https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution/{slug}',
            headers={
                'Content-Type': 'application/json',
                'authorization': f'Bearer {self._token}'
            },
            data=dumps(upload_ids)
        )
        if res.status_code != 200:
            raise Exception(f'{res.status_code} - Error executing quick command on Stackspot: {res.text}')
        self._id = res.json()
        return self

    def get_callback(self):
        if self._id is None:
            raise Exception('ID response from quick command execution not present')

        status = 'RUNNING'
        response = None
        now = datetime.now()
        expired = now + timedelta(seconds=16)

        while status != 'COMPLETED' or now > expired:
            time.sleep(5)
            res = requests.get(
                url=f'https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{self._id}',
                headers={
                    'authorization': f'Bearer {self._token}'
                }
            )
            if res.status_code != 200:
                raise Exception('Callback error')
            status = res.json().get('progress', {}).get('status')
            response = res.json()
        return response
