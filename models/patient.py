import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
class HmsPatient(models.Model):
    _name = "hms.patient"
    _description = "Hospital Patient"
    _rec_name = "first_name"

    _sql_constraints = [
        ('unique_patient_email', 'UNIQUE(email)', 'The email address must be unique for each patient!')
    ]

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email")
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")

    cr_ratio = fields.Float(string="CR Ratio")

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Type")

    pcr = fields.Boolean(string="PCR")

    image = fields.Binary(string="Image")

    address = fields.Text(string="Address")

    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    department_id = fields.Many2one("hms.department", string="Department" , domain="[('is_opened', '=', True)]")

    department_capacity = fields.Integer(related="department_id.capacity")

    doctor_ids = fields.Many2many("hms.doctor", string="Doctors")

    log_ids = fields.One2many("hms.patient.log","patient_id")

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    @api.depends("birth_date")
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0
    

    @api.onchange('birth_date')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically'
                }
            }
        
    @api.onchange('state')
    def _onchange_state(self):

        if self.state:

              self.log_ids += self.env['hms.patient.log'].new({
                  'description': f'State changed to {self.state}'
              })


    @api.constrains('email')
    def _check_valid_email(self):
        for rec in self:
            if rec.email:
                email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if not re.match(email_regex, rec.email):
                    raise ValidationError("Invalid Email Address! Please enter a valid email format (e.g., example@domain.com).")
                
                duplicate_email = self.search([('email', '=', rec.email), ('id', '!=', rec.id)])
                if duplicate_email:
                    raise ValidationError("The email address must be unique for each patient!")