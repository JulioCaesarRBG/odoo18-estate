from odoo import models, api


class RealEstateCustomReport(models.AbstractModel):
    _name = 'report.estate.report_real_estate_custom_document'
    _description = 'Real Estate Custom Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get values for custom real estate report"""
        if not docids and data:
            docids = data.get('ids', [])
        
        docs = self.env['real.estate'].browse(docids)
        
        form_data = data.get('form', {}) if data else {}
        
        return {
            'doc_ids': docids,
            'doc_model': 'real.estate',
            'docs': docs,
            'data': form_data,
            'show_property_details': form_data.get('show_property_details', True),
            'show_price_info': form_data.get('show_price_info', True),
            'show_contact_info': form_data.get('show_contact_info', True),
            'show_specifications': form_data.get('show_specifications', True),
            'show_garden': form_data.get('show_garden', True),
            'show_tags': form_data.get('show_tags', True),
            'show_description': form_data.get('show_description', True),
            'show_offers': form_data.get('show_offers', False),
            'include_images': form_data.get('include_images', True),
            'group_by_type': form_data.get('group_by_type', False),
        }
