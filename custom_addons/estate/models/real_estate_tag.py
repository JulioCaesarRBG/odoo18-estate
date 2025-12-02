from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'real.estate.tag'
    _inherit = 'real.estate.mixin'
    _description = 'Real Estate Tag Model'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]
    _order = 'name asc'

    name = fields.Char(required=True)
    color = fields.Integer()