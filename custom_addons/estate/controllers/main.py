from odoo import http
from odoo.http import request

class CustomController(http.Controller):
    @http.route('/estate/get_info', auth='public', type='http', website=True)
    def get_info(self, **kw):
        examples = request.env["real.estate"].sudo().search([])
        data = []
        for rec in examples:
            data.append({
                "id": rec.id,
                "name": rec.name,
                "selling_price": rec.selling_price,
                "description": rec.description,
                "state": rec.state,
            })

        values = {
            "status": "success",
            "count": len(data),
            "results": data
        }
        return request.render('estate.example_json_page', values)


    @http.route('/estate/page', auth='public', website=True)
    def page(self, **kw):
    # render template q.v. views/templates.xml
        values = {'message': 'Hello from Odoo 18 controller!'}
        return request.render('estate.template_page', values)


    @http.route('/estate/create_partner', auth='user', type='json', methods=['POST'])
    def create_partner(self, **post):
        name = post.get('name')
        if not name:
            return {'error': 'name is required'}
        partner = request.env['res.partner'].sudo().create({'name': name})
        return {'id': partner.id, 'name': partner.name}