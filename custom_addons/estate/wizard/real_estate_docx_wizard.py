from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import os
from ..services.docx_pdf_service import DocxPdfService
from ..services.email_service import EmailService

class RealEstateManualDocxWizard(models.TransientModel):
    _name = 'real.estate.manual.docx.wizard'
    _description = 'Real Estate Manual Generate DOCX Wizard'

    name = fields.Char('Nama', required=True)
    email = fields.Char('Email', required=True)
    generated_pdf = fields.Binary('Generated PDF', readonly=True)
    generated_pdf_filename = fields.Char('PDF Filename')

    def action_generate_pdf(self):
        template_path = '/root/projects/odoo18/custom_addons/estate/static/src/tmp/certificate_template.docx'
        context = {'name': self.name or ''}
        pdf_data, pdf_filename = DocxPdfService.generate_pdf_from_template(template_path, context, self.name)
        self.generated_pdf = pdf_data
        self.generated_pdf_filename = pdf_filename
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_send_pdf_email(self):
        if not self.generated_pdf:
            raise UserError('Please generate the PDF file before sending.')
            
            raise UserError('Email address is missing. Please provide a valid email.')

        EmailService.send_pdf_email(self.env, self.email, self.generated_pdf, self.generated_pdf_filename)
    
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'The PDF has been successfully sent to %s.' % self.email,
                'type': 'success',
                'sticky': False,
            }
        }

