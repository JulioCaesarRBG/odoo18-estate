from odoo import models, fields, api , _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from ..services.offer_estate_service import OfferEstateService

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
        """Compute the deadline date based on validity"""
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Inverse method to update validity based on date_deadline"""
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        """Accept offer"""
        self.ensure_one()
        service = OfferEstateService(self.env)
        service.accept_offer(self.id)
    
    def refuse_offer(self):
        """Refuse offer"""
        self.ensure_one()
        service = OfferEstateService(self.env)
        service.refuse_offer(self.id)

    @api.model_create_multi
    def create(self, vals_list):
        """Create offer with validations and update property state"""
        service = OfferEstateService(self.env)
        
        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                service.validate_new_offer(vals['property_id'], vals['price'])
    
        res = super().create(vals_list)
        for record in res:
            service.update_property_state_on_offer(record.property_id.id)
        
        return res

