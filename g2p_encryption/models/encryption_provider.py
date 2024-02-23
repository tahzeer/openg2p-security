from odoo import api, fields, models


class G2PEncryptionProvider(models.Model):
    _name = "g2p.encryption.provider"
    _description = "G2P Encryption Provider"

    name = fields.Char(required=True)
    type = fields.Selection(selection="_selection_provider_type")

    @api.model
    def _selection_provider_type(self):
        return []

    def encrypt_data(self, data, **kwargs):
        raise NotImplementedError()

    def decrypt_data(self, data, **kwargs):
        raise NotImplementedError()

    def sign_jwt(self, data, **kwargs):
        raise NotImplementedError()

    def verifiy_jwt(self, data, **kwargs):
        raise NotImplementedError()

    def get_jwks(self, **kwargs):
        raise NotImplementedError()
