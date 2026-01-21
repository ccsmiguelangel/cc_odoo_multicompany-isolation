from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        # Get website company if available
        website_company_id = None
        try:
            from odoo.http import request
            if request and hasattr(request, 'env'):
                website = request.env['website'].sudo().get_current_website()
                if website and website.company_id:
                    website_company_id = website.company_id.id
        except Exception:
            pass
        
        for vals in vals_list:
            if not vals.get('company_id'):
                # Use website company if available, otherwise use user's company
                vals['company_id'] = website_company_id or self.env.company.id
        return super().create(vals_list)
