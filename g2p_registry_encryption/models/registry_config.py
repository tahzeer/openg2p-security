from odoo import api, fields, models


class RegistryConfigDecrypt(models.TransientModel):

    _inherit = "res.config.settings"

    decrypt_fields = fields.Boolean("Decrypt Fields", default=False, store=True)
    # partner_name = fields.Char(
    #     string="Partner Name",
    #     related="partner_id.name",
    #     store=False,
    #     readonly=True,
    # )

    def set_values(self):
        res = super(RegistryConfigDecrypt, self).set_values()
        params = self.env["ir.config_parameter"].sudo()
        params.set_param("g2p_registry.decrypt_fields", self.decrypt_fields)
        return res

    @api.model
    def get_values(self):
        res = super(RegistryConfigDecrypt, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            decrypt_fields=params.get_param(
                "g2p_registry.decrypt_fields", default=False
            ),
        )
        return res
