from odoo import models, fields, api , _
from odoo.exceptions import UserError
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
    
    _order = 'price desc'

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

    def accept_offer(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Only one offer can be accepted for a property."))
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
    
    def refuse_offer(self):
        self.ensure_one()
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                existing_offers = self.search([('property_id', '=', vals['property_id'])])
                if existing_offers:
                    max_existing_price = max(existing_offers.mapped('price'))
                    if vals['price'] <= max_existing_price:
                        raise UserError(_("The offer amount must be higher than the existing offers (%.2f).") % max_existing_price)
    
        res = super().create(vals_list)
        for record in res:
            record.property_id.state = 'received'
        
        return res

