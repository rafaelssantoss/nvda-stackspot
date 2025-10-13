from .stackspot_auth import StackspotAuth
from .stackspot_upload_file import StackspotFile
from .stackspot_agent import StackspotAgent


class Stackspot:
    _instance = None

    def __init__(self):
        self._realm = None
        self._client_secret = None
        self._client_id = None
        self._targe_id = None
        self._context = None
        self._file = None
        self.auth = None
        self.upload = None

    @staticmethod
    def instance():
        if Stackspot._instance is None:
            Stackspot._instance = Stackspot()
        return Stackspot._instance

    def credential(self, client_id, client_secret, realm):
        self._client_id = client_id
        self._client_secret = client_secret
        self._realm = realm
        self.auth = StackspotAuth(self._client_id, self._client_secret, self._realm)
        return self

    def send_file_stackspot(self, file, context, targe_id):
        self._file = file
        self._context = context
        self._targe_id = targe_id
        self.upload = StackspotFile(self._file, self._context, self._targe_id)
        return self

    def transcription(self, agent_id):
        token = self.auth.get_access_token()
        self.upload.file_upload(token)
        file_id = self.upload.get_file_id()

        if file_id is None:
            raise Exception('Error getting file id in Stackspot')

        response = (StackspotAgent(agent_id, token).agent().execute(
            {
                "streaming": False,
                "user_prompt": "",
                "stackspot_knowledge": False,
                "return_ks_in_response": True,
                "upload_ids": [file_id]
            }
        ))

        result = response.get('message')
        if result is None:
            return 'Error'
        else:
            return result
