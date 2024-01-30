import base64
from odoo import fields

from odoo import models, fields, api
from odoo.addons.g2p_encryption.models.keymanager_api import EncryptionModule, OdooAuth


class EncryptedPartner(models.Model):
    _inherit = "res.partner"

    is_encrypted = fields.Boolean("Is encrypted?")

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
            encoded_field_value = base64.b64encode(field_value.encode()).decode()
            encrypted_data = encryption_module_instance.encrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": encoded_field_value,
                }
            )
            return encrypted_data

        vals["name"] = encrypt_field(vals.get("name")) if vals.get("name") else None
        vals["family_name"] = (
            encrypt_field(vals.get("family_name")) if vals.get("family_name") else None
        )
        vals["given_name"] = (
            encrypt_field(vals.get("given_name")) if vals.get("given_name") else None
        )
        vals["addl_name"] = (
            encrypt_field(vals.get("addl_name")) if vals.get("addl_name") else None
        )
        vals["display_name"] = (
            encrypt_field(vals.get("display_name"))
            if vals.get("display_name")
            else None
        )
        vals["email"] = encrypt_field(vals.get("email")) if vals.get("email") else None
        vals["phone"] = encrypt_field(vals.get("phone")) if vals.get("phone") else None
        vals["mobile"] = (
            encrypt_field(vals.get("mobile")) if vals.get("mobile") else None
        )
        vals["address"] = (
            encrypt_field(vals.get("address")) if vals.get("address") else None
        )
        vals["birth_place"] = (
            encrypt_field(vals.get("birth_place")) if vals.get("birth_place") else None
        )
        vals["is_encrypted"] = bool(vals.get("name"))

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

        for record in self:
            if "name" in vals:
                vals["name"] = (
                    encrypt_field(vals.get("name")) if vals.get("name") else None
                )
            if "family_name" in vals:
                vals["family_name"] = (
                    encrypt_field(vals.get("family_name"))
                    if vals.get("family_name")
                    else None
                )
            if "given_name" in vals:
                vals["given_name"] = (
                    encrypt_field(vals.get("given_name"))
                    if vals.get("given_name")
                    else None
                )
            if "addl_name" in vals:
                vals["addl_name"] = (
                    encrypt_field(vals.get("addl_name"))
                    if vals.get("addl_name")
                    else None
                )
            if "display_name" in vals:
                vals["display_name"] = (
                    encrypt_field(vals.get("display_name"))
                    if vals.get("display_name")
                    else None
                )
            if "email" in vals:
                vals["email"] = (
                    encrypt_field(vals.get("email")) if vals.get("email") else None
                )
            if "phone" in vals:
                vals["phone"] = (
                    encrypt_field(vals.get("phone")) if vals.get("phone") else None
                )
            if "mobile" in vals:
                vals["mobile"] = (
                    encrypt_field(vals.get("mobile")) if vals.get("mobile") else None
                )
            if "address" in vals:
                vals["address"] = (
                    encrypt_field(vals.get("address")) if vals.get("address") else None
                )
            if "birth_place" in vals:
                vals["birth_place"] = (
                    encrypt_field(vals.get("birth_place"))
                    if vals.get("birth_place")
                    else None
                )

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
                if "name" in record and record["name"]:
                    decrytt = decrypt_field(record["name"])
                    self.env.cache.set(record, self._fields["name"], decrytt)
                if "family_name" in record and record["family_name"]:
                    decrytt = decrypt_field(record["family_name"])
                    self.env.cache.set(record, self._fields["family_name"], decrytt)
                if "addl_name" in record and record["addl_name"]:
                    decrytt = decrypt_field(record["addl_name"])
                    self.env.cache.set(record, self._fields["addl_name"], decrytt)
                if "display_name" in record and record["display_name"]:
                    decrytt = decrypt_field(record["display_name"])
                    self.env.cache.set(record, self._fields["display_name"], decrytt)
                if "given_name" in record and record["given_name"]:
                    decrytt = decrypt_field(record["given_name"])
                    self.env.cache.set(record, self._fields["given_name"], decrytt)
                if "email" in record and record["email"]:
                    decrytt = decrypt_field(record["email"])
                    self.env.cache.set(record, self._fields["email"], decrytt)
                if "phone" in record and record["phone"]:
                    decrytt = decrypt_field(record["phone"])
                    self.env.cache.set(record, self._fields["phone"], decrytt)
                if "address" in record and record["address"]:
                    decrytt = decrypt_field(record["address"])
                    self.env.cache.set(record, self._fields["address"], decrytt)
                if "birth_place" in record and record["birth_place"]:
                    decrytt = decrypt_field(record["birth_place"])
                    self.env.cache.set(record, self._fields["birth_place"], decrytt)
                if "birth_place" in record and record["birth_place"]:
                    decrytt = decrypt_field(record["birth_place"])
                    self.env.cache.set(record, self._fields["birth_place"], decrytt)
                # if "is_encrypted" in record:
                #     record["is_encrypted"] = False
                    



# def read(self, fields=None, load="_classic_read"):
#     odoo_token = {
#         "auth_url": "https://keycloak.dev.openg2p.net/realms/openg2p/protocol/openid-connect/token",
#         "auth_client_id": "openg2p-admin-client",
#         "auth_client_secret": "x75SU2hqKQX7IPob",
#         "auth_grant_type": "client_credentials",
#     }

#     odoo_auth = OdooAuth(**odoo_token)
#     base_url = "https://dev.openg2p.net/v1/keymanager"
#     encryption_module_instance = EncryptionModule(base_url, odoo_auth)
#     application_id = "REGISTRATION"
#     reference_id = ""

#     def decrypt_field(field_value):
#         decrypted_data = encryption_module_instance.decrypt_data(
#             {
#                 "applicationId": application_id,
#                 "referenceId": reference_id,
#                 "data": field_value,
#             }
#         )
#         while len(decrypted_data) % 4 != 0:
#             decrypted_data += "="
#         decoded_value = base64.b64decode(decrypted_data).decode("utf-8")
#         return decoded_value

#     is_decrypt_fields_enabled = self.env["ir.config_parameter"].get_param(
#         "g2p_registry.decrypt_fields", default=False
#     )
#     records = super(EncryptedPartner, self).read(fields=fields, load=load)

#     for record in records:
#         if is_decrypt_fields_enabled:
#             if "name" in record:
#                 record["name"] = (
#                     decrypt_field(record.get("name"))
#                     if record.get("name")
#                     else None
#                 )
#             if "family_name" in record:
#                 record["family_name"] = (
#                     decrypt_field(record.get("family_name"))
#                     if record.get("family_name")
#                     else None
#                 )
#             if "given_name" in record:
#                 record["given_name"] = (
#                     decrypt_field(record.get("given_name"))
#                     if record.get("given_name")
#                     else None
#                 )
#             if "addl_name" in record:
#                 record["addl_name"] = (
#                     decrypt_field(record.get("addl_name"))
#                     if record.get("addl_name")
#                     else None
#                 )
#             if "display_name" in record:
#                 record["display_name"] = (
#                     decrypt_field(record.get("display_name"))
#                     if record.get("display_name")
#                     else None
#                 )
#             if "email" in record:
#                 record["email"] = (
#                     decrypt_field(record.get("email"))
#                     if record.get("email")
#                     else None
#                 )
#             # if "phone" in record:
#             #     record["phone"] = (
#             #         decrypt_field(record.get("phone"))
#             #         if record.get("phone")
#             #         else None
#             #     )

#             if "address" in record:
#                 record["address"] = (
#                     decrypt_field(record.get("address"))
#                     if record.get("address")
#                     else None
#                 )
#             if "birth_place" in record:
#                 record["birth_place"] = (
#                     decrypt_field(record.get("birth_place"))
#                     if record.get("birth_place")
#                     else None
#                 )
#             if "is_encrypted" in record:
#                 record["is_encrypted"] = False
#     # print("========going to registry or encyrtping", records)
#     return records
