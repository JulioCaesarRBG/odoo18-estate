from odoo import models, fields, api , _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

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
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    'warning': {
                        'title': _("warning"),
                        'message': _("the availability date cannot be set in the past."),
                    }
                }

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("A canceled property cannot be set as sold."))
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("A sold property cannot be canceled."))
            record.state = 'canceled'

    @api.constrains('selling_price', 'expected_price')
    def _check_constraint(self):
        for record in self:
            if record.selling_price and record.selling_price < (record.expected_price * 90) / 100:
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(_("Only properties with state 'New' or 'Canceled' can be deleted."))