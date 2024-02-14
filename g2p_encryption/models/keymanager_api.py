from datetime import datetime

import requests


class OdooAuth(object):
    def __init__(self, auth_url, auth_client_id, auth_client_secret, auth_grant_type):
        self.auth_url = auth_url
        self.auth_client_id = auth_client_id
        self.auth_client_secret = auth_client_secret
        self.auth_grant_type = auth_grant_type

    def get_access_token(self):
        data = {
            "client_id": self.auth_client_id,
            "client_secret": self.auth_client_secret,
            "grant_type": self.auth_grant_type,
        }
        response = requests.post(self.auth_url, data=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            response.raise_for_status()


# odoo_token = {
#     "auth_url": "https://keycloak.dev.openg2p.net/realms/mosip/protocol/openid-connect/token",
#     "auth_client_id": "mosip-admin-client",
#     "auth_client_secret": "F42OX9zwiaUfzwsk",
#     "auth_grant_type": "client_credentials",
# }

# odoo_auth = OdooAuth(**odoo_token)
# access_token = odoo_auth.get_access_token()
# print(f"Access Token: {access_token}")


class EncryptionModule(object):
    def __init__(self, base_url, odoo_auth):
        self.base_url = base_url
        self.access_token = odoo_auth.get_access_token()
        self.current_time = self.generate_current_time()

    def generate_current_time(self):
        # Generate current timestamp in ISO 8601 format
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def get_certificate(self, data):
        url = f"{self.base_url}/getCertificate"
        headers = {"Cookie": f"Authorization={self.access_token}"}

        params = {
            "applicationId": data.get("applicationId", "string"),
            "referenceId": data.get("referenceId", "string"),
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json().get("response", {}).get("certificate", None)

    def encrypt_data(self, data):
        url = f"{self.base_url}/encrypt"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "timeStamp": self.current_time,
                "data": data.get("data", "string"),
                "salt": "string",
                "aad": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        # print(response.content)

        return response.json().get("response", {}).get("data", None)

    def jwt_encrypt_data(self, data):
        url = f"{self.base_url}/jwtencrypt"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "data": "string",
                "enableDefCompression": True,
                "includeCertificate": True,
                "includeCertHash": True,
                "jwkSetUrl": "string",
                "x509Certificate": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def jwt_decrypt_data(self, data):
        url = f"{self.base_url}/jwtdecrypt"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "encData": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def decrypt_data(self, data):
        url = f"{self.base_url}/decrypt"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "timeStamp": self.current_time,
                "data": data.get("data", "string"),
                "salt": "string",
                "aad": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        response = response.json().get("response", {})
        if response:
            response = response.get("data", {})
        return response
        # response = requests.post(url, json=payload, headers=headers)
        # print(response.content)

        # return response.json().get("response", {}).get("data", None)

    def get_signing_public_key(self):
        url = f"{self.base_url}/getSigningPublicKey"
        headers = {"Cookie": f"Authorization={self.access_token}"}

        response = requests.get(url, headers=headers)
        return response.json()

    def get_encryption_public_key(self):
        url = f"{self.base_url}/getEncryptionPublicKey"
        headers = {"Cookie": f"Authorization={self.access_token}"}

        response = requests.get(url, headers=headers)
        return response.json()

    def encrypt_data_with_pin(self, data):
        url = f"{self.base_url}/encryptWithPin"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {"data": "string", "userPin": "string"},
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def decrypt_data_with_pin(self, data):
        url = f"{self.base_url}/decryptWithPin"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {"data": "string", "userPin": "string"},
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def jwt_verify(self, data):
        url = f"{self.base_url}/jwtVerify"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "jwtSignatureData": "string",
                "actualData": "string",
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "certificateData": "string",
                "validateTrust": True,
                "domain": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def jwt_sign(self, data):
        url = f"{self.base_url}/jwtSign"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "dataToSign": data.get("dataToSign", "string"),
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "includePayload": True,
                # "includeCertificate": True,
                # "includeCertHash": True,
                # "certificateUrl": data.get("certificateUrl", "string"),
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        try:
            jwt_signed_data = (
                response.json().get("response", {}).get("jwtSignedData", None)
            )
        except ValueError:
            # print("Error parsing response JSON. JWT signing failed.")
            jwt_signed_data = None

        return jwt_signed_data

    def jws_sign(self, data):
        url = f"{self.base_url}/jwsSign"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "dataToSign": "string",
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "includePayload": True,
                "includeCertificate": True,
                "includeCertHash": True,
                "certificateUrl": "string",
                "validateJson": True,
                "b64JWSHeaderParam": True,
                "signAlgorithm": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def generate_masterkey_optional(self, data, object_type):
        url = f"{self.base_url}/generateMasterKey/{object_type}"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "force": True,
                "commonName": "string",
                "organizationUnit": "string",
                "organization": "string",
                "location": "string",
                "state": "string",
                "country": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def generate_csr(self, data):
        url = f"{self.base_url}/generateCsr"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": data.get("applicationId", "string"),
                "referenceId": data.get("referenceId", "string"),
                "commonName": "string",
                "organizationUnit": "string",
                "organization": "string",
                "location": "string",
                "state": "string",
                "country": "string",
            },
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def generate_symmetric_key(self, data):
        url = f"{self.base_url}/generateSymmetricKey"
        headers = {"Cookie": f"Authorization={self.access_token}"}
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": self.current_time,
            "metadata": {},
            "request": {
                "applicationId": "string",
                "referenceId": "string",
                "force": True,
            },
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
