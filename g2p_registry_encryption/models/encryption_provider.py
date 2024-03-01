from odoo import api, models


class RegistryEncryptionProvider(models.Model):
    _inherit = "g2p.encryption.provider"

    @api.model
    def set_registry_provider(self, provider_id, replace=True):
        if provider_id and (
            replace
            or not self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_encryption.encryption_provider_id", None)
        ):
            self.env["ir.config_parameter"].sudo().set_param(
                "g2p_registry_encryption.encryption_provider_id", str(provider_id)
            )

    @api.model
    def get_registry_provider(self):
        prov_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_encryption.encryption_provider_id", None)
        )
        return self.browse(int(prov_id)) if prov_id else None
