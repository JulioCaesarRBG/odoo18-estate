from odoo import _
from odoo.exceptions import UserError, ValidationError


class EstateService:
    """Service layer untuk business logic Real Estate"""

    def __init__(self, env):
        self.env = env

    def sell_property(self, property_id):
        """Set property as sold"""
        property_rec = self.env['real.estate'].browse(property_id)
        
        if property_rec.state == 'canceled':
            raise UserError(_("A canceled property cannot be set as sold."))
        
        property_rec.state = 'sold'

    def cancel_property(self, property_id):
        """Cancel property"""
        property_rec = self.env['real.estate'].browse(property_id)
        
        if property_rec.state == 'sold':
            raise UserError(_("A sold property cannot be canceled."))
        
        property_rec.state = 'canceled'

    def validate_selling_price(self, selling_price, expected_price):
        """Validate selling price is at least 90% of expected price"""
        if selling_price and selling_price < (expected_price * 90) / 100:
            raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))

    def validate_delete(self, state):
        """Validate property can only be deleted if state is new or canceled"""
        if state not in ('new', 'canceled'):
            raise UserError(_("Only properties with state 'New' or 'Canceled' can be deleted."))
