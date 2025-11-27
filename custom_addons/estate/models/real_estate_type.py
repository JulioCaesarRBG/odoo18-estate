from odoo import models, fields

class propertyType(models.Model):
    _name = 'real.estate.type'
    _description = 'Real Estate Type Model'

    name = fields.Char(string="Name", required=True)