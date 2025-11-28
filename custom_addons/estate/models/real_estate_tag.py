from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag Model'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]

    name = fields.Char(required=True)