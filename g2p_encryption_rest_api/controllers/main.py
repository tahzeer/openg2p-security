from odoo.addons.base_rest.controllers.main import RestController


class SecurityController(RestController):
    _root_path = "/api/v1/security/"
    _collection_name = "base.rest.security.services"
    _default_auth = "user"
