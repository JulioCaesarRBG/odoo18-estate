import os
import base64
import subprocess
import tempfile
from docxtpl import DocxTemplate

class DocxPdfService:
    @staticmethod
    def generate_pdf_from_template(template_path, context, output_name):
        if not os.path.exists(template_path):
            raise FileNotFoundError(f'Template file not found: {template_path}')
        doc = DocxTemplate(template_path)
        doc.render(context)
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_docx:
            doc.save(tmp_docx.name)
            docx_path = tmp_docx.name
        pdf_path = docx_path.replace('.docx', '.pdf')
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(docx_path), docx_path
        ], check=True)
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        return base64.b64encode(pdf_data), f"{output_name or 'document'}.pdf"
