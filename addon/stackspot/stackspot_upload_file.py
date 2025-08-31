import requests
from json import dumps


class StackspotFile:
    def __init__(self, file, context, target_id):
        self.file = file
        self.context = context
        self.target_id = target_id

    def get_file_id(self):
        return self._id

    def _form_upload(self, token) -> dict:
        res = requests.post(
            url='https://data-integration-api.stackspot.com/v2/file-upload/form',
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json',
                'authorization': f'Bearer {token}'
            },
            data=dumps({
                'file_name': '81292.jpg',
                'target_type': self.context,
                'target_id': self.target_id
            })
        )
        if res.status_code != 201:
            raise Exception(f'{res.status_code} - Error creating form to file upload on Stackspot: {res.text}')

        data = res.json()
        self._id = data.get('id')
        return {
            'url': data.get('url'),
            'key': data.get('form', {}).get('key'),
            'x-amz-algorithm': data.get('form', {}).get('x-amz-algorithm'),
            'x-amz-credential': data.get('form', {}).get('x-amz-credential'),
            'x-amz-date': data.get('form', {}).get('x-amz-date'),
            'x-amz-security-token': data.get('form', {}).get('x-amz-security-token'),
            'x-amz-signature': data.get('form', {}).get('x-amz-signature'),
            'policy': data.get('form', {}).get('policy')
        }

    def file_upload(self, token):
        form_response = self._form_upload(token)

        res = requests.post(
            url=form_response['url'],
            files={
                'file': self.file
            },
            data={
                'key': form_response.get('key'),
                'x-amz-algorithm': form_response.get('x-amz-algorithm'),
                'x-amz-credential': form_response.get('x-amz-credential'),
                'x-amz-date': form_response.get('x-amz-date'),
                'x-amz-security-token': form_response.get('x-amz-security-token'),
                'x-amz-signature': form_response.get('x-amz-signature'),
                'policy': form_response.get('policy')
            }
        )
        if res.status_code != 204:
            raise Exception(f'{res.status_code} - Error sending file upload on Stackspot: {res.text}')
