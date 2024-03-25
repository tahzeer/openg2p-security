import logging

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class WellknownRestService(Component):
    _name = "security_well_known.rest.service"
    _inherit = ["base.rest.service"]
    _usage = ".well-known"
    _collection = "base.rest.security.services"
    _description = """
        Security Well-Known API Services
    """

    @restapi.method(
        [
            (
                [
                    "/jwks.json",
                ],
                "GET",
            )
        ],
        auth="public",
    )
    def get_jwks(self):
        encryption_providers = self.env["g2p.encryption.provider"].sudo().search([])
        jwks = []
        for prov in encryption_providers:
            try:
                prov_jwks = prov.get_jwks()
                jwks.extend(prov_jwks.get("keys", []) if prov_jwks else [])
            except Exception:
                _logger.exception("Unable to get JWKS from list of encryption providers")
        return {"keys": jwks}
