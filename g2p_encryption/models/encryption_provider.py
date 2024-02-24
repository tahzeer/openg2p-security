from odoo import fields, models


class G2PEncryptionProvider(models.Model):
    _name = "g2p.encryption.provider"
    _description = "G2P Encryption Provider"

    name = fields.Char(required=True)
    type = fields.Selection(selection=[])

    def encrypt_data(self, data: bytes, **kwargs) -> bytes:
        """
        Both input and output are NOT base64 encoded
        """
        raise NotImplementedError()

    def decrypt_data(self, data: bytes, **kwargs) -> bytes:
        """
        Both input and output are NOT base64 encoded
        """
        raise NotImplementedError()

    def jwt_sign(
        self,
        data: dict,
        include_payload=True,
        include_certificate=True,
        include_cert_hash=True,
        **kwargs
    ) -> str:
        raise NotImplementedError()

    def jwt_verify(self, data: str, **kwargs) -> dict:
        raise NotImplementedError()

    def get_jwks(self, **kwargs):
        raise NotImplementedError()
