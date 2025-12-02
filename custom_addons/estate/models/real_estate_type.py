from odoo import models, fields, api, _

class propertyType(models.Model):
    _name = 'real.estate.type'
    _inherit = ['real.estate.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Type Model'
    _order = 'sequence desc'

    sequence = fields.Integer(default=1)
    # name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('real.estate', 'property_type_id')
    offer_ids = fields.One2many('real.estate.offer', 'type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    property_count = fields.Integer(compute='_compute_property_count')

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env['real.estate.tag'].create(
                {
                    'name': vals.get('name')
                }
            )
        return res

    def unlink(self):
        self.property_ids.state = 'canceled'
        return super().unlink()

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)   

    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)

    def action_open_property_ids(self):
        return {
            'name': _('Related Properties'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'real.estate',
            'domain': [('property_type_id', '=', self.id)],
            "context": {'default_property_type_id': self.id},
        }

    def action_open_offer_ids(self):
        return {
            'name': _('Related Offers'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'real.estate.offer',
            'domain': [('type_id', '=', self.id)],
            "context": {'default_type_id': self.id},
        }
