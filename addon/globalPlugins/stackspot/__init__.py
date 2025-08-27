from logHandler import log
import os
import requests
import uuid

REALM: str = "stackspot-freemium"
CLIENT_ID: str= "teste"
CLIENT_SECRET: str = "teste"
#TOKEN_URL: str = f"http://localhost:8080/{REALM}/oidc/oauth/token"
TOKEN_URL: str = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"

#CHAT_URL = "http://localhost:8080/v1/agent/01JS0SSFDKPYXATPQ1J9RAW3B2/chat"
CHAT_URL = "https://genai-inference-app.stackspot.com/v1/agent/01JS0SSFDKPYXATPQ1J9RAW3B2/chat"

#FORM_UPLOAD_URL = "http://localhost:8080/v2/file-upload/form"
FORM_UPLOAD_URL: str = "https://data-integration-api.stackspot.com/v2/file-upload/form"

class Stackspot:
	def __init__(self):
		self.jwt = None

	def authenticate(self, client_id: str, client_secret: str) -> str:
		response = requests.post(TOKEN_URL, data={
			"grant_type": "client_credentials",
			"client_id": client_id,
			"client_secret": client_secret
		})
		response.raise_for_status()

		json = response.json()
		return json["access_token"]

	def upload_image(self, file: str):
		file_basename = os.path.basename(file)
		response = requests.post(FORM_UPLOAD_URL, headers={
			"Authorization": f"Bearer {self.jwt}"
		},
		json={
			"file_name": file_basename,
			"target_type": "CONTEXT",
			"expiration": 60
		})
		json = response.json()
		log.info(json)
		response.raise_for_status()

		upload_url = json["url"]

		log.info(F"Subindo imagem para {upload_url}")

		with open(file, "rb") as f:
			image_bytes = f.read()
			content_response = requests.post(upload_url, headers={
			}, data={
				"key": json["form"]["key"],
				"x-amz-credential": json["form"]["x-amz-credential"],
				"x-amz-algorithm": json["form"]["x-amz-algorithm"],
				"x-amz-date": json["form"]["x-amz-date"],
				"x-amz-security-token": json["form"]["x-amz-security-token"],
				"policy": json["form"]["policy"],
				"x-amz-signature": json["form"]["x-amz-signature"],
				"file": image_bytes
			})
			log.info(content_response.content)
			content_response.raise_for_status()

			return json()["id"]

	def _get_description(self, image_id: str, prompt: str) -> str:
		chat_response = requests.post(CHAT_URL, headers={
			"Authorization": f"Bearer {self.jwt}"
		},
		json={
			"streaming": False,
			"user_prompt": prompt,
			"stackspot_knowledge": False,
			"return_ks_in_response": True,
			"upload_ids": [image_id]
		})

		return chat_response.json()["message"]

	def describe_image(self, image_bytes: bytes):
		if not self.jwt:
			log.info("Autenticando na Stackspot...")
			self.jwt = self.authenticate(CLIENT_ID, CLIENT_SECRET)
			log.info("Autenticado com sucesso")

		image_id = self.upload_image(image_bytes)
		log.info(f"Imagem de {image_id} criada com sucesso")

		return self._get_description(image_id, "Quais informações estão contidas nesta imagens?")
