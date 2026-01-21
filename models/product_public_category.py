import json
import time

from odoo import models, api, fields
from odoo.tools.sql import column_exists


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        index=True,
    )

    def _auto_init(self):
        # region agent log
        with open('/home/odoo/.cursor/debug.log', 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'pre',
                'hypothesisId': 'H1',
                'location': 'addons/multicompany_isolation/models/product_public_category.py:_auto_init:18',
                'message': 'Auto init entry for product.public.category',
                'data': {
                    'db': self.env.registry.db_name,
                    'has_company_id_column': column_exists(self.env.cr, 'product_public_category', 'company_id'),
                },
                'timestamp': int(time.time() * 1000),
            }) + '\n')
        # endregion
        result = super()._auto_init()
        # region agent log
        with open('/home/odoo/.cursor/debug.log', 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'pre',
                'hypothesisId': 'H1',
                'location': 'addons/multicompany_isolation/models/product_public_category.py:_auto_init:30',
                'message': 'Auto init exit for product.public.category',
                'data': {
                    'db': self.env.registry.db_name,
                    'has_company_id_column': column_exists(self.env.cr, 'product_public_category', 'company_id'),
                },
                'timestamp': int(time.time() * 1000),
            }) + '\n')
        # endregion
        return result

    @api.model_create_multi
    def create(self, vals_list):
        # region agent log
        with open('/home/odoo/.cursor/debug.log', 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'pre',
                'hypothesisId': 'H2',
                'location': 'addons/multicompany_isolation/models/product_public_category.py:create:45',
                'message': 'Create public categories',
                'data': {
                    'vals_count': len(vals_list),
                    'missing_company_id': sum(1 for vals in vals_list if not vals.get('company_id')),
                },
                'timestamp': int(time.time() * 1000),
            }) + '\n')
        # endregion
        for vals in vals_list:
            if not vals.get('company_id'):
                vals['company_id'] = self.env.company.id
        records = super().create(vals_list)
        # region agent log
        with open('/home/odoo/.cursor/debug.log', 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'pre',
                'hypothesisId': 'H2',
                'location': 'addons/multicompany_isolation/models/product_public_category.py:create:60',
                'message': 'Created public categories',
                'data': {
                    'record_ids': records.ids,
                },
                'timestamp': int(time.time() * 1000),
            }) + '\n')
        # endregion
        return records
