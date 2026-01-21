from odoo import models, api, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    public_categ_ids = fields.Many2many(
        string="Website Product Category",
        help="The product will be available in each mentioned eCommerce category. Go to Shop > Edit"
             " Click on the page and enable 'Categories' to view all eCommerce categories.",
        comodel_name='product.public.category',
        relation='product_public_category_product_template_rel',
        domain=lambda self: [('company_id', 'in', self.env.companies.ids)],
        check_company=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('company_id'):
                vals['company_id'] = self.env.company.id
        return super().create(vals_list)
