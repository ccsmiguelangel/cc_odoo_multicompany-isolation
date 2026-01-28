from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        # Determinar la empresa correcta basándose en el contexto (backend vs frontend)
        target_company_id = None
        is_frontend = False
        
        try:
            from odoo.http import request
            if request and hasattr(request, 'httprequest'):
                path = request.httprequest.path or ''
                # Rutas de backend - usar empresa del usuario
                backend_prefixes = ('/web', '/jsonrpc', '/xmlrpc', '/longpolling', '/mail', '/bus', '/websocket')
                is_backend_path = any(path.startswith(prefix) for prefix in backend_prefixes)
                
                if not is_backend_path and hasattr(request, 'env'):
                    # Frontend (eCommerce, portal) - usar empresa del website
                    website = request.env['website'].sudo().get_current_website()
                    if website and website.company_id:
                        target_company_id = website.company_id.id
                        is_frontend = True
        except Exception:
            pass
        
        # Si es backend o no hay website, usar la empresa actual del usuario
        if not is_frontend:
            target_company_id = self.env.company.id
        
        for vals in vals_list:
            if not vals.get('company_id'):
                vals['company_id'] = target_company_id
        
        return super().create(vals_list)
