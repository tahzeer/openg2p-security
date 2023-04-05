
from odoo import fields

from odoo import models, fields, api
from odoo.addons.g2p_encryption.models.crypto import AESCipher

class EncryptedPhoneNumber(models.Model):
    _inherit = "g2p.phone.number"
    
    phone_no_decrypted = fields.Char(compute=lambda self:self._decrypt_field("phone_no", "phone_no_decrypted"), store=False)
    



    @api.model
    def create(self, vals):
        record = super(EncryptedPhoneNumber, self).create(vals)
        #TODO encryption key should be moved to a secret vault.
        encryption_key = self.env['ir.config_parameter'].get_param('g2p_enc_key', '')
        if encryption_key:
            crypto = AESCipher(encryption_key)
            record["phone_no"] = crypto.encrypt(record["phone_no"]) if record["phone_no"] else None

        return record
    
    
    def _decrypt_field(self,actual_field, decrypted_field) :
        #TODO encryption key should be moved to a secret vault.
        encryption_key = self.env['ir.config_parameter'].get_param('g2p_enc_key', '')
        if encryption_key:
            crypto = AESCipher(encryption_key)
            for rec in self:
                if rec[actual_field] :
                    rec[decrypted_field] = crypto.decrypt(rec[actual_field]) 
                else:
                    rec[decrypted_field] = ''
                print(decrypted_field,",",rec[decrypted_field])  
