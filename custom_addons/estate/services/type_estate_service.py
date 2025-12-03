from odoo import _


class TypeEstateService:
    """Service layer untuk business logic Real Estate Type"""

    def __init__(self, env):
        self.env = env

    def create_tag_from_type(self, type_name):
        """Create tag with same name as type"""
        self.env['real.estate.tag'].create({'name': type_name})

    def cancel_properties_on_delete(self, property_ids):
        """Cancel all properties when type is deleted"""
        properties = self.env['real.estate'].browse(property_ids)
        properties.write({'state': 'canceled'})
