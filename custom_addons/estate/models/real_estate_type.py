from odoo import models, fields, api

class propertyType(models.Model):
    _name = 'real.estate.type'
    _description = 'Real Estate Type Model'
    _order = 'sequence desc'

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('real.estate', 'property_type_id')
    offer_ids = fields.One2many('real.estate.offer', 'type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)   
