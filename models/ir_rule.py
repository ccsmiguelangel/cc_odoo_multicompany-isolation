from odoo import models, api
from odoo.http import request
from odoo.fields import Domain
import json, time

# #region agent log
def _debug_log(loc, msg, data, hyp):
    try:
        with open('/home/odoo/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({'location': loc, 'message': msg, 'data': data, 'hypothesisId': hyp, 'timestamp': int(time.time()*1000), 'sessionId': 'debug'}) + '\n')
    except: pass
# #endregion


class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def _compute_domain(self, model_name, mode="read"):
        """
        Override para res.partner: Aplicar aislamiento por empresa.
        
        Reglas:
        - Usuarios internos (partner_share=False): siempre visibles (necesario para mail, seguidores)
        - Contactos externos (partner_share=True): solo visibles si son de la empresa actual
        - El propio partner del usuario: siempre visible
        """
        if model_name == 'res.partner':
            user = self.env.user
            company_id = self.env.company.id
            context_company_ids = self.env.context.get('allowed_company_ids', [company_id])
            user_partner_id = user.partner_id.id
            
            # Para administradores: usar TODAS sus empresas asignadas
            # Para otros usuarios: usar solo las empresas del contexto (seleccionadas)
            is_admin = user.has_group('base.group_system')
            if is_admin:
                company_ids = user.company_ids.ids if user.company_ids else context_company_ids
            else:
                company_ids = context_company_ids
            
            # #region agent log
            path = ''
            try:
                path = request.httprequest.path if request and hasattr(request, 'httprequest') else ''
            except: pass
            _debug_log('ir_rule:_compute_domain', 'Domain check', {
                'user': user.login,
                'user_id': user.id,
                'is_admin': is_admin,
                'env_company_id': company_id,
                'context_allowed_company_ids': context_company_ids,
                'final_company_ids': company_ids,
                'user_partner_id': user_partner_id,
                'path': path
            }, 'H1')
            # #endregion
            
            return Domain([
                '|', '|',
                ('partner_share', '=', False),
                ('company_id', 'in', company_ids),
                ('id', '=', user_partner_id)
            ])
        
        return super()._compute_domain(model_name, mode)

    @api.model
    def _eval_context(self):
        """
        Extend to use website company for frontend, or user's current company for backend.
        Applies to ALL users, including admins.
        """
        eval_context = super()._eval_context()
        
        website_company_id = None
        is_frontend = False
        
        try:
            if request and hasattr(request, 'httprequest'):
                path = request.httprequest.path or ''
                backend_prefixes = ('/web', '/jsonrpc', '/xmlrpc', '/longpolling', '/mail', '/bus', '/websocket')
                is_backend_path = any(path.startswith(prefix) for prefix in backend_prefixes)
                
                if not is_backend_path and hasattr(request, 'env'):
                    website = request.env['website'].sudo().get_current_website()
                    if website and website.company_id:
                        website_company_id = website.company_id.id
                        is_frontend = True
        except Exception:
            pass
        
        if is_frontend and website_company_id:
            eval_context['company_id'] = website_company_id
            eval_context['company_ids'] = [website_company_id]
        else:
            current_company = self.env.company.id
            allowed_companies = self.env.context.get('allowed_company_ids', [current_company])
            eval_context['company_id'] = current_company
            eval_context['company_ids'] = allowed_companies
        
        return eval_context
