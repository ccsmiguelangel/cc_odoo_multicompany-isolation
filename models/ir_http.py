from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _pre_dispatch(cls, rule, arguments):
        """Extend to set company context based on website domain for backend routes."""
        super()._pre_dispatch(rule, arguments)
        
        # Only apply if we have a request with website context and a valid user
        if not request or not hasattr(request, 'env'):
            return
            
        user = request.env.user
        # Ensure we have a valid user singleton
        if not user or len(user) != 1:
            return
            
        # Get current website based on domain
        try:
            website = request.env['website'].sudo().get_current_website()
        except Exception:
            return
            
        if not website or not website.company_id:
            return
        
        website_company_id = website.company_id.id
        user_company_ids = user._get_company_ids()
        
        # Check if user is internal and has access to this company
        try:
            is_internal = user._is_internal()
            has_access = website_company_id in user_company_ids
            
            if is_internal and has_access:
                # Force the website's company as the active company for this request
                request.update_context(
                    allowed_company_ids=[website_company_id],
                )
        except Exception:
            pass
