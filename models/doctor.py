from odoo import models, fields, api

class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _description = "Hospital Doctor"
    _rec_name = "first_name"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)

    image = fields.Binary(string="Image")

    patient_ids = fields.Many2many("hms.patient",string="Patients")

