from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag Model'

    name = fields.Char(required=True)