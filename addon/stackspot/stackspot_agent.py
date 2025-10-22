import requests
from json import dumps


class StackspotAgent:

    def __init__(self, agent_id, token):
        self._agent_id = agent_id
        self._token = token

    def agent(self):
        return self

    def execute(self, body: dict):
        res = requests.post(
            url=f'https://genai-inference-app.stackspot.com/v1/agent/{self._agent_id}/chat',
            headers={
                'Content-Type': 'application/json',
                'authorization': f'Bearer {self._token}'
            },
            data=dumps(body)
        )
        if res.status_code != 200:
            raise Exception(f'{res.status_code} - Error executing agent on Stackspot: {res.text}')
        return res.json()
