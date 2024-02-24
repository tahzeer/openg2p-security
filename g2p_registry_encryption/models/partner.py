import json

from odoo import api, fields, models


class EncryptedPartner(models.Model):
    _inherit = "res.partner"

    encrypted_val = fields.Binary("Encrypted value", attachment=False)
    is_encrypted = fields.Boolean(default=False)

    fields_list_to_enc = [
        "name",
        "family_name",
        "given_name",
        "addl_name",
        "display_name",
        "address",
        "birth_place",
    ]

    placeholder_to_encrypted_field = "encrypted"

    @api.model
    def gather_fields_to_be_enc_from_dict(
        self,
        fields_dict: dict,
        replace=True,
    ):
        to_be_enc = {}
        for each in self.fields_list_to_enc:
            if fields_dict.get(each, None):
                to_be_enc[each] = fields_dict[each]
                if replace:
                    fields_dict[each] = self.placeholder_to_encrypted_field
        return to_be_enc

    def create(self, vals_list):
        prov = self.env["g2p.encryption.provider"].get_registry_provider()
        is_encrypt_fields = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_encryption.encrypt_registry", default=False)
        )
        for vals in vals_list:
            if is_encrypt_fields and (vals.get("is_registrant", False)):
                to_be_encrypted = self.gather_fields_to_be_enc_from_dict(vals)
                vals["encrypted_val"] = prov.encrypt_data(
                    json.dumps(to_be_encrypted).encode()
                )
                vals["is_encrypted"] = True

        return super().create(vals_list)

    def write(self, vals_list):
        prov = self.env["g2p.encryption.provider"].get_registry_provider()
        is_encrypt_fields = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_encryption.encrypt_registry", default=False)
        )
        rec_values_list = self.read(self.fields_list_to_enc + "is_registrant")
        for rec, vals in zip(rec_values_list, vals_list):
            if is_encrypt_fields and (
                rec.get("is_registrant", False) or vals.get("is_registrant", False)
            ):
                vals = rec.update(vals)
                to_be_encrypted = self.gather_fields_to_be_enc_from_dict(vals)

                vals["encrypted_val"] = prov.encrypt_data(
                    json.dumps(to_be_encrypted).encode()
                )
                vals["is_encrypted"] = True

        return super().write(vals_list)

    def _read(self, fields):
        res = super()._read(fields)
        prov = self.env["g2p.encryption.provider"].get_registry_provider()
        is_decrypt_fields = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_encryption.decrypt_registry", default=False)
        )
        for record in self:
            if is_decrypt_fields and record.is_encrypted and record.encrypted_val:
                decrypted_vals = json.loads(
                    prov.decrypt_data(record.encrypted_val).decode()
                )

                for field_name in self.fields_list_to_enc:
                    if field_name in record and record[field_name]:
                        self.env.cache.set(
                            record, self._fields[field_name], decrypted_vals[field_name]
                        )
        return res
