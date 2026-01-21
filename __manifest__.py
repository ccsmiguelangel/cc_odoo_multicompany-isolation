{
    'name': 'Multi-company Isolation (Partners & Products)',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'Ensures strict multi-company isolation for partners and products.',
    'depends': ['base', 'product', 'website_sale'],
    'data': [
        'security/record_rules.xml',
    ],
    'author': 'Miguel Peña <miguel.angel@exagon.es>',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
