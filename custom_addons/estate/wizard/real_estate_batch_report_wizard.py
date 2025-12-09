from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RealEstateBatchReportWizard(models.TransientModel):
    _name = 'real.estate.batch.report.wizard'
    _description = 'Real Estate Custom Print Wizard'

    property_ids = fields.Many2many(
        'real.estate', 
        'wizard_property_rel',
        'wizard_id',
        'property_id',
        string='Properties to Print',
        required=True
    )
    
    show_property_details = fields.Boolean(string='Property Details', default=True)
    show_price_info = fields.Boolean(string='Price Information', default=True)
    show_contact_info = fields.Boolean(string='Contact Information', default=True)
    show_specifications = fields.Boolean(string='Specifications', default=True)
    show_garden = fields.Boolean(string='Garden Information', default=True)
    show_tags = fields.Boolean(string='Tags', default=True)
    show_description = fields.Boolean(string='Description', default=True)
    show_offers = fields.Boolean(string='Offers List', default=False)
    
    include_images = fields.Boolean(string='Include Company Logo', default=True)
    group_by_type = fields.Boolean(string='Group by Property Type', default=False)
    sort_by = fields.Selection([
        ('name', 'Name'),
        ('date', 'Date Availability'),
        ('price', 'Expected Price'),
        ('state', 'Status'),
    ], string='Sort By', default='name')
    
    property_count = fields.Integer(string='Properties Count', compute='_compute_property_count')
    
    @api.depends('property_ids')
    def _compute_property_count(self):
        """Compute count of properties"""
        for wizard in self:
            wizard.property_count = len(wizard.property_ids)
    
    @api.model
    def default_get(self, fields_list):
        """Set default selected properties from context"""
        res = super().default_get(fields_list)
        
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['property_ids'] = [(6, 0, active_ids)]
        
        return res
    
    def action_print_report(self):
        """Generate and print custom report"""
        self.ensure_one()
        
        if not self.property_ids:
            raise UserError(_('Please select at least one property to print.'))
        
        properties = self.property_ids
        if self.sort_by == 'date':
            properties = properties.sorted(key=lambda p: p.date_availability or fields.Date.today())
        elif self.sort_by == 'price':
            properties = properties.sorted(key=lambda p: p.expected_price, reverse=True)
        elif self.sort_by == 'state':
            properties = properties.sorted(key=lambda p: p.state)
        else:
            properties = properties.sorted(key=lambda p: p.name)
        
        data = {
            'ids': properties.ids,
            'model': 'real.estate',
            'form': {
                'show_property_details': self.show_property_details,
                'show_price_info': self.show_price_info,
                'show_contact_info': self.show_contact_info,
                'show_specifications': self.show_specifications,
                'show_garden': self.show_garden,
                'show_tags': self.show_tags,
                'show_description': self.show_description,
                'show_offers': self.show_offers,
                'include_images': self.include_images,
                'group_by_type': self.group_by_type,
            }
        }
        
        return self.env.ref('estate.action_report_real_estate_custom').report_action(properties, data=data)
