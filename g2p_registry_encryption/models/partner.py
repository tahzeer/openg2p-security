import base64
import json

from odoo import api, fields, models

from odoo.addons.g2p_encryption.models.keymanager_api import EncryptionModule, OdooAuth


class EncryptedPartner(models.Model):
    _inherit = "res.partner"

    is_encrypted = fields.Boolean("Is encrypted?")
    encrypted_val = fields.Char("Encrypted value")
    # encrypted_val = fields.Binary("Encrypted value")

    @api.model
    def create(self, vals):
        odoo_token = {
            "auth_url": "https://keycloak.dev.openg2p.net/realms/openg2p/protocol/openid-connect/token",
            "auth_client_id": "openg2p-admin-client",
            "auth_client_secret": "x75SU2hqKQX7IPob",
            "auth_grant_type": "client_credentials",
        }

        odoo_auth = OdooAuth(**odoo_token)
        base_url = "https://dev.openg2p.net/v1/keymanager"
        encryption_module_instance = EncryptionModule(base_url, odoo_auth)
        application_id = "REGISTRATION"
        reference_id = "string"

        def encrypt_field(field_value):
            json_data = json.dumps(field_value)
            encoded_field_value = base64.b64encode((json_data).encode()).decode()
            encrypted_data = encryption_module_instance.encrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": encoded_field_value,
                }
            )
            return encrypted_data

        vals["is_encrypted"] = bool(vals.get("name"))
        vals["encrypted_val"] = encrypt_field(vals)

        vals["name"] = "encrypted"
        vals["family_name"] = "encrypted"
        vals["given_name"] = "encrypted"
        vals["addl_name"] = "encrypted"
        vals["display_name"] = "encrypted"
        vals["address"] = "encrypted"
        vals["birth_place"] = "encrypted"
        # for field, value in vals.items():
        #     if isinstance(value, str):
        #         vals[field] = "encrypted"
        record = super(EncryptedPartner, self).create(vals)
        return record

    def write(self, vals):
        odoo_token = {
            "auth_url": "https://keycloak.dev.openg2p.net/realms/openg2p/protocol/openid-connect/token",
            "auth_client_id": "openg2p-admin-client",
            "auth_client_secret": "x75SU2hqKQX7IPob",
            "auth_grant_type": "client_credentials",
        }

        odoo_auth = OdooAuth(**odoo_token)
        base_url = "https://dev.openg2p.net/v1/keymanager"
        encryption_module_instance = EncryptionModule(base_url, odoo_auth)
        application_id = "REGISTRATION"
        reference_id = "string"

        def encrypt_field(field_value):
            encoded_field_value = base64.b64encode(field_value.encode()).decode()
            encrypted_data = encryption_module_instance.encrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": encoded_field_value,
                }
            )
            return encrypted_data

        vals["is_encrypted"] = bool(vals.get("name"))
        vals["encrypted_val"] = encrypt_field(vals)
        if "name" in vals:
            vals["name"] = "encrypted"
        if "family_name" in vals:
            vals["family_name"] = "encrypted"
        if "given_name" in vals:
            vals["given_name"] = "encrypted"
        if "addl_name" in vals:
            vals["addl_name"] = "encrypted"
        if "display_name" in vals:
            vals["display_name"] = "encrypted"
        if "address" in vals:
            vals["address"] = "encrypted"
        if "birth_place" in vals:
            vals["birth_place"] = "encrypted"

        result = super(EncryptedPartner, self).write(vals)
        return result

    def _read(self, fields):
        odoo_token = {
            "auth_url": "https://keycloak.dev.openg2p.net/realms/openg2p/protocol/openid-connect/token",
            "auth_client_id": "openg2p-admin-client",
            "auth_client_secret": "x75SU2hqKQX7IPob",
            "auth_grant_type": "client_credentials",
        }

        odoo_auth = OdooAuth(**odoo_token)
        base_url = "https://dev.openg2p.net/v1/keymanager"
        encryption_module_instance = EncryptionModule(base_url, odoo_auth)
        application_id = "REGISTRATION"
        reference_id = ""

        def decrypt_field(field_value):
            decrypted_data = encryption_module_instance.decrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": field_value,
                }
            )
            while decrypted_data and len(decrypted_data) % 4 != 0:
                decrypted_data += "="
            if field_value and not decrypted_data:
                return field_value
            decoded_value = base64.b64decode(decrypted_data).decode("utf-8")

            return decoded_value

        is_decrypt_fields_enabled = self.env["ir.config_parameter"].get_param(
            "g2p_registry.decrypt_fields", default=False
        )
        super(EncryptedPartner, self)._read(fields)
        for record in self:
            if is_decrypt_fields_enabled and record["is_encrypted"]:
                d = decrypt_field(record["encrypted_val"])
                decrytt = json.loads(d)
                # print(decrytt["name"])

                if "name" in record and record["name"]:
                    self.env.cache.set(record, self._fields["name"], decrytt["name"])
                if "family_name" in record and record["family_name"]:
                    self.env.cache.set(
                        record, self._fields["family_name"], decrytt["family_name"]
                    )
                if "addl_name" in record and record["addl_name"]:
                    self.env.cache.set(
                        record, self._fields["addl_name"], decrytt["addl_name"]
                    )
                if "given_name" in record and record["given_name"]:
                    self.env.cache.set(
                        record, self._fields["given_name"], decrytt["given_name"]
                    )
                if "display_name" in record and record["name"]:
                    self.env.cache.set(
                        record,
                        self._fields["display_name"],
                        decrytt["name"],
                    )
                if "email" in record and record["email"]:
                    self.env.cache.set(record, self._fields["email"], decrytt["email"])
