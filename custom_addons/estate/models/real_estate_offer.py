from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

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
    type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
    
