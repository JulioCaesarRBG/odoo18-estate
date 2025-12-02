from odoo import models, fields, api , _

class estateOffer(models.Model):
    _inherit = 'real.estate.offer'

    account_move_id = fields.Many2one('account.move')
    