from odoo import models, fields, api , _

class estateMixin(models.AbstractModel):
    _name = 'real.estate.mixin'

    name = fields.Char(required=True)