from odoo import models, fields ,api
from odoo.exceptions import ValidationError , UserError

class ResPartnerITI(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one(
        "hms.patient",
        string="Related Patient"
    )

    @api.constrains('related_patient_id')
    def _check_unique_patient_email(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email:
                patient_email = partner.related_patient_id.email
                
                duplicate_partner = self.search([
                    ('id', '!=', partner.id), 
                    ('related_patient_id.email', '=', patient_email) 
                ])
                
                if duplicate_partner:
                    raise ValidationError(
                        f"Validation Error! The patient's email ({patient_email}) is already assigned to another customer: '{duplicate_partner.name}'."
                    )
                
    
    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise UserError(
                    f"Action Restricted! You cannot delete the customer '{partner.name}' as they are linked to a patient ({partner.related_patient_id.first_name})."
                )
        return super(ResPartner, self).unlink()

