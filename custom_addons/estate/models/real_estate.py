from odoo import models, fields, api , _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from ..services.estate_service import EstateService

class RealEstate(models.Model):
    _name = 'real.estate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Model'

    active = fields.Boolean(default=True, invisible=False)
    name = fields.Char(required=True)
    state = fields.Selection(
        [
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
        ], 
        required=True,
        copy=False,
        default='new'
    )
    
    def _default_date(self):
        return fields.Date.today()

    _order = 'id desc'

    post_code = fields.Char() 
    date_availability = fields.Date(default=_default_date)
    expected_price = fields.Float()
    best_offer = fields.Float(compute="_compute_best_offer")
    selling_price = fields.Float(readonly=True)
    buyer_id = fields.Many2one('res.partner', copy=False, readonly=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    description = fields.Text()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")

    property_type_id = fields.Many2one('real.estate.type')
    offer_ids = fields.One2many('real.estate.offer', 'property_id')
    tag_ids = fields.Many2many('real.estate.tag', string='Tags')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Compute total area as sum of living area and garden area"""
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        """Compute the best offer price for the property"""
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        """Reset garden area and orientation if garden is False"""
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        """Warn if availability date is set in the past"""
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    'warning': {
                        'title': _("warning"),
                        'message': _("the availability date cannot be set in the past."),
                    }
                }

    def action_sold(self):
        """Mark property as sold"""
        service = EstateService(self.env)
        for record in self:
            service.sell_property(record.id)

    def action_cancel(self):
        """Cancel property"""
        service = EstateService(self.env)
        for record in self:
            service.cancel_property(record.id)

    @api.constrains('selling_price', 'expected_price')
    def _check_constraint(self):
        """Validate selling price is at least 90% of expected price"""
        service = EstateService(self.env)
        for record in self:
            service.validate_selling_price(record.selling_price, record.expected_price)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        """Validate property can only be deleted if state is new or canceled"""
        service = EstateService(self.env)
        for record in self:
            service.validate_delete(record.state)