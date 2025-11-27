from odoo import models, fields

class estateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = 'Real Estate Offer Model'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required= True)
    property_id = fields.Many2one('real.estate', required= True)
