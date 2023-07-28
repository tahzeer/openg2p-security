import logging

from odoo import api, fields, models

from odoo.addons.g2p_encryption.models.crypto import AESCipher

_logger = logging.getLogger(__name__)


class EncryptedRegID(models.Model):
    _inherit = "g2p.reg.id"

    value_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("value", "value_decrypted"),
        store=False,
    )

    @api.model
    def create(self, vals):
        record = super(EncryptedRegID, self).create(vals)
        # TODO encryption key should be moved to a secret vault.
        encryption_key = self.env["ir.config_parameter"].get_param("g2p_enc_key", "")
        if encryption_key:
            crypto = AESCipher(encryption_key)
            record["value"] = (
                crypto.encrypt(record["value"]) if record["value"] else None
            )

        return record

    def _decrypt_field(self, actual_field, decrypted_field):
        # TODO encryption key should be moved to a secret vault.
        encryption_key = self.env["ir.config_parameter"].get_param("g2p_enc_key", "")
        if encryption_key:
            crypto = AESCipher(encryption_key)
            for rec in self:
                if rec[actual_field]:
                    rec[decrypted_field] = crypto.decrypt(rec[actual_field])
                else:
                    rec[decrypted_field] = ""
                _logger.info("%s , %s", decrypted_field, rec[decrypted_field])
