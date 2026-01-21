from odoo import models, api
from odoo.http import request
from odoo.orm.domains import Domain

# Modelos afectados por las reglas de aislamiento multicompañía de este módulo
ISOLATION_MODELS = {'res.partner', 'product.template', 'product.product', 'product.public.category'}


class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def _compute_domain(self, model_name, mode="read"):
        """
        Override to apply multicompany isolation rules.
        Admins get bypass ONLY in backend, not in frontend (website context).
        """
        user = self.env.user
        is_admin = False
        is_frontend = False
        
        try:
            is_admin = user.has_group('base.group_system')
        except Exception:
            pass
        
        # Check if we're in a frontend/website context
        try:
            if request and hasattr(request, 'env'):
                website = request.env['website'].sudo().get_current_website()
                is_frontend = bool(website)
        except Exception:
            pass
        
        # Solo bypass para admins en el BACKEND (no frontend)
        # En el frontend, todos deben respetar el aislamiento por empresa
        if is_admin and model_name in ISOLATION_MODELS and not is_frontend:
            return Domain.TRUE
        
        result = super()._compute_domain(model_name, mode)
        return result

    @api.model
    def _eval_context(self):
        """Extend to include website company for multi-website isolation."""
        eval_context = super()._eval_context()
        
        # Skip for admin users (they need full access to manage all companies)
        user = self.env.user
        try:
            is_admin = user.has_group('base.group_system')
            if is_admin:
                return eval_context
        except Exception:
            pass
        
        # Try to get the current website's company
        website_company_id = None
        try:
            if request and hasattr(request, 'env'):
                website = request.env['website'].sudo().get_current_website()
                if website and website.company_id:
                    website_company_id = website.company_id.id
        except Exception:
            pass
        
        # If we have a website company, use it; otherwise fall back to user's company
        if website_company_id:
            eval_context['company_id'] = website_company_id
            eval_context['company_ids'] = [website_company_id]
        
        return eval_context
