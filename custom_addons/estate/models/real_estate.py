from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class RealEstate(models.Model):
    _name = 'real.estate'
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

    post_code = fields.Char() 
    date_availability = fields.Date(default=_default_date)
    expected_price = fields.Float()
    best_offer = fields.Float(compute="_compute_best_offer")
    selling_price = fields.Float()
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
    tag_ids = fields.Many2many('real.estate.tag')

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

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # @api.depends('validity')
    # def _compute_date_deadline(self):
    #     for record in self:
    #         record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    # def _inverse_date_deadline(self):
    #     for record in self:
    #         record.validity = (record.date_deadline - fields.Date.today()).days     