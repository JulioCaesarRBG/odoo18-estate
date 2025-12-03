from odoo import _, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class OfferEstateService:
    """Service layer untuk business logic Real Estate Offer"""

    def __init__(self, env):
        self.env = env

    def accept_offer(self, offer_id):
        """Accept offer"""
        offer = self.env['real.estate.offer'].browse(offer_id)
        
        if "accepted" in offer.property_id.offer_ids.mapped('status'):
            raise UserError(_("Only one offer can be accepted for a property."))
        
        offer.status = 'accepted'
        offer.property_id.selling_price = offer.price
        offer.property_id.buyer_id = offer.partner_id
        offer.property_id.state = 'accepted'

    def refuse_offer(self, offer_id):
        """Refuse offer"""
        offer = self.env['real.estate.offer'].browse(offer_id)
        offer.status = 'refused'

    def validate_new_offer(self, property_id, price):
        """Validate offer price against existing offers"""
        existing_offers = self.env['real.estate.offer'].search([('property_id', '=', property_id)])
        if existing_offers:
            max_existing_price = max(existing_offers.mapped('price'))
            if price <= max_existing_price:
                raise UserError(_("The offer amount must be higher than the existing offers (%.2f).") % max_existing_price)

    def update_property_state_on_offer(self, property_id):
        """Update property state to 'received' when offer is created"""
        property_rec = self.env['real.estate'].browse(property_id)
        property_rec.state = 'received'