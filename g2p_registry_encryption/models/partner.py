# import logging

# from odoo import api, fields, models

# from odoo.addons.g2p_encryption.models.crypto import AESCipher

# _logger = logging.getLogger(__name__)


# class EncryptedPartner(models.Model):
#     _inherit = "res.partner"

#     # is_encrypted = fields.Boolean("Is encrypted?")

#     name_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("name", "name_decrypted"), store=False
#     )
#     family_name_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field(
#             "family_name", "family_name_decrypted"
#         ),
#         store=False,
#     )
#     given_name_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("given_name", "given_name_decrypted"),
#         store=False,
#     )
#     addl_name_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("addl_name", "addl_name_decrypted"),
#         store=False,
#     )
#     email_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("email", "email_decrypted"),
#         store=False,
#     )
#     phone_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("phone", "phone_decrypted"),
#         store=False,
#     )
#     mobile_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("mobile", "mobile_decrypted"),
#         store=False,
#     )
#     address_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field("address", "address_decrypted"),
#         store=False,
#     )
#     birth_place_decrypted = fields.Char(
#         compute=lambda self: self._decrypt_field(
#             "birth_place", "birth_place_decrypted"
#         ),
#         store=False,
#     )

#     @api.model
#     def create(self, vals):
#         record = super(EncryptedPartner, self).create(vals)
#         # TODO encryption key should be moved to a secret vault.
#         encryption_key = self.env["ir.config_parameter"].get_param("g2p_enc_key", "")
#         if encryption_key:
#             crypto = AESCipher(encryption_key)
#             record["name"] = crypto.encrypt(record["name"]) if record["name"] else None
#             record["family_name"] = (
#                 crypto.encrypt(record["family_name"]) if record["family_name"] else None
#             )
#             record["given_name"] = (
#                 crypto.encrypt(record["given_name"]) if record["given_name"] else None
#             )
#             record["addl_name"] = (
#                 crypto.encrypt(record["addl_name"]) if record["addl_name"] else None
#             )
#             record["display_name"] = (
#                 crypto.encrypt(record["display_name"])
#                 if record["display_name"]
#                 else None
#             )
#             record["email"] = (
#                 crypto.encrypt(record["email"]) if record["email"] else None
#             )
#             record["phone"] = (
#                 crypto.encrypt(record["phone"]) if record["phone"] else None
#             )
#             record["mobile"] = (
#                 crypto.encrypt(record["mobile"]) if record["mobile"] else None
#             )
#             record["address"] = (
#                 crypto.encrypt(record["address"]) if record["address"] else None
#             )
#             record["birth_place"] = (
#                 crypto.encrypt(record["birth_place"]) if record["birth_place"] else None
#             )

#         return record

#     # @api.model
#     # def write(self, vals):
#     #     record = super(EncryptedPartner, self).create(vals)
#     #     #TODO encryption key should be moved to a secret vault.
#     #     encryption_key = self.env['ir.config_parameter'].get_param('g2p_enc_key', '')
#     #     if encryption_key:
#     #         crypto = AESCipher(encryption_key)
#     #         record["name"] = crypto.encrypt(record["name"]) if record["name"] else None
#     #         record["family_name"] = crypto.encrypt(record["family_name"]) if record["family_name"] else None
#     #         record["given_name"] = crypto.encrypt(record["given_name"]) if record["given_name"] else None
#     #         record["addl_name"] = crypto.encrypt(record["addl_name"]) if record["addl_name"] else None
#     #         record["display_name"] = crypto.encrypt(record["display_name"]) if record["display_name"] else None
#     #         record["email"] = crypto.encrypt(record["email"]) if record["email"] else None
#     #         record["phone"] = crypto.encrypt(record["phone"]) if record["phone"] else None
#     #         record["mobile"] = crypto.encrypt(record["mobile"]) if record["mobile"] else None
#     #         record["address"] = crypto.encrypt(record["address"]) if record["address"] else None
#     #         record["birth_place"] = crypto.encrypt(record["birth_place"]) if record["birth_place"] else None

#     #     return record

#     def _decrypt_field(self, actual_field, decrypted_field):
#         # TODO encryption key should be moved to a secret vault.
#         encryption_key = self.env["ir.config_parameter"].get_param("g2p_enc_key", "")
#         if encryption_key:
#             crypto = AESCipher(encryption_key)
#             for rec in self:
#                 if rec[actual_field]:
#                     rec[decrypted_field] = crypto.decrypt(rec[actual_field])
#                 else:
#                     rec[decrypted_field] = ""
#                 _logger.info("%s , %s", decrypted_field, rec[decrypted_field])


import base64
from odoo import fields

from odoo import models, fields, api
from odoo.addons.g2p_encryption.models.keymanager_api import EncryptionModule, OdooAuth


class EncryptedPartner(models.Model):
    _inherit = "res.partner"

    # is_encrypted = fields.Boolean("Is encrypted?")

    name_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("name", "name_decrypted"), store=False
    )
    family_name_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field(
            "family_name", "family_name_decrypted"
        ),
        store=False,
    )
    given_name_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("given_name", "given_name_decrypted"),
        store=False,
    )
    addl_name_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("addl_name", "addl_name_decrypted"),
        store=False,
    )
    email_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("email", "email_decrypted"),
        store=False,
    )
    phone_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("phone", "phone_decrypted"),
        store=False,
    )
    mobile_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("mobile", "mobile_decrypted"),
        store=False,
    )
    address_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field("address", "address_decrypted"),
        store=False,
    )
    birth_place_decrypted = fields.Char(
        compute=lambda self: self._decrypt_field(
            "birth_place", "birth_place_decrypted"
        ),
        store=False,
    )

    @api.model
    def create(self, vals):
        record = super(EncryptedPartner, self).create(vals)
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

        # access_token = odoo_auth.get_access_token()
        # print(f"Access Token: {access_token}")

        def encrypt_field(field_value):
            encoded_field_value = base64.b64encode(field_value.encode()).decode()
            # print(f"Original Field Value: {field_value}")
            encrypted_data = encryption_module_instance.encrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": encoded_field_value,
                }
            )
            return encrypted_data

        record["name"] = encrypt_field(record["name"]) if record["name"] else None
        record["family_name"] = (
            encrypt_field(record["family_name"]) if record["family_name"] else None
        )
        record["given_name"] = (
            encrypt_field(record["given_name"]) if record["given_name"] else None
        )
        record["addl_name"] = (
            encrypt_field(record["addl_name"]) if record["addl_name"] else None
        )
        record["display_name"] = (
            encrypt_field(record["display_name"]) if record["display_name"] else None
        )
        record["email"] = encrypt_field(record["email"]) if record["email"] else None
        record["phone"] = encrypt_field(record["phone"]) if record["phone"] else None
        record["mobile"] = encrypt_field(record["mobile"]) if record["mobile"] else None
        record["address"] = (
            encrypt_field(record["address"]) if record["address"] else None
        )
        record["birth_place"] = (
            encrypt_field(record["birth_place"]) if record["birth_place"] else None
        )

        print("create methoddd", record)
        return record

    def _decrypt_field(self, actual_field, decrypted_field):
        odoo_token = {
            "auth_url": "https://keycloak.dev.openg2p.net/realms/mosip/protocol/openid-connect/token",
            "auth_client_id": "openg2p-admin-client",
            "auth_client_secret": "x75SU2hqKQX7IPob",
            "auth_grant_type": "client_credentials",
        }

        odoo_auth = OdooAuth(**odoo_token)
        base_url = "https://dev.openg2p.net/v1/keymanager"
        encryption_module_instance = EncryptionModule(base_url, odoo_auth)
        application_id = "KERNEL"
        reference_id = "SIGN"

        def decrypt_field(field_value):
            return encryption_module_instance.decrypt_data(
                {
                    "applicationId": application_id,
                    "referenceId": reference_id,
                    "data": field_value,
                }
            )

        for rec in self:
            if rec[actual_field]:
                rec[decrypted_field] = decrypt_field(rec[actual_field])
            else:
                rec[decrypted_field] = ""
            # print(decrypted_field, ",", rec[decrypted_field])
