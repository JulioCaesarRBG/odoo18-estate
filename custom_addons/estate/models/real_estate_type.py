from odoo import models, fields, api, _
from ..services.type_estate_service import TypeEstateService

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
        """Create property type and associated tag"""
        res = super().create(vals_list)
        service = TypeEstateService(self.env)
        
        for vals in vals_list:
            service.create_tag_from_type(vals.get('name'))
        
        return res

    def unlink(self):
        """Cancel all properties when type is deleted"""
        service = TypeEstateService(self.env)
        service.cancel_properties_on_delete(self.property_ids.ids)
        return super().unlink()

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """Compute the number of offers associated with this type"""
        for record in self:
            record.offer_count = len(record.offer_ids)   

    @api.depends('property_ids')
    def _compute_property_count(self):
        """Compute the number of properties associated with this type"""
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
