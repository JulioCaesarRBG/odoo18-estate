from odoo import models, fields, api , _

class estateUsers(models.Model):
    _inherit = 'res.users'

    property_type_ids = fields.One2many(
        'real.estate',
        'salesperson_id',
        string="Properties"
    )