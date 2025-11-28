from odoo import models, fields

class propertyType(models.Model):
    _name = 'real.estate.type'
    _description = 'Real Estate Type Model'



    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('real.estate', 'property_type_id')