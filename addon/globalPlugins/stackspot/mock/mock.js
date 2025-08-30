const express = require("express")

const app = express()

app.post("/teste/oidc/oauth/token", (request, response) => {
	return response.json({"access_token": "abc123"});
});

app.post("/v2/file-upload/form", (request, response) => {
	return response.json({
		"url": "http://localhost:8080/imagem",
		"form": {
			"key": "minhachave",
			"x-amz-credential": "cred123",
			"x-amz-algorithm": "alg123",
			"x-amz-date": "data123",
			"x-amz-security-token": "token123",
			"policy": "policy",
			"x-amz-signature": "sig"
		}
	});
})

app.post("/imagem", (request, response) => response.json({"id": "imagem123"}));

app.post("/v1/agent/01JS0SSFDKPYXATPQ1J9RAW3B2/chat", (request, response) => response.json({"message": "funciona"}));

app.listen(8080, () => console.log("Mock pronto"));
