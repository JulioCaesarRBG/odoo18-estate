from odoo import models, fields

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
    best_offer = fields.Float()
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
    total_area = fields.Integer(string="Total Area (sqm)")

    property_type_id = fields.Many2one('real.estate.type')
    offer_ids = fields.One2many('real.estate.offer', 'property_id')
    tag_ids = fields.Many2many('real.estate.tag')