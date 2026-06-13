from odoo import models, fields

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')

    blood_type = fields.Selection([
        ('a_pos', 'A+'),
        ('a_neg', 'A-'),
        ('b_pos', 'B+'),
        ('b_neg', 'B-'),
        ('o_pos', 'O+'),
        ('o_neg', 'O-'),
        ('ab_pos', 'AB+'),
        ('ab_neg', 'AB-')
    ], string='Blood Type')

    pcr = fields.Boolean(string='PCR Positive')

    image = fields.Image(string='Patient Image')

    address = fields.Text(string='Address')

    age = fields.Integer(string='Age')