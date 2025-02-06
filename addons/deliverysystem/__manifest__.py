# -*- coding: utf-8 -*-
{
    'name': "Delivery System",
    'summary': "Module to extend Odoo for delivery management",
    'description': """
Long description of module's purpose
    """,
    'author': "Osman Elsahib",
    'website': "https://www.dflex.co.uk",
    'category': 'Delivery',
    'version': '0.1',
    'depends': ['base',"sale", "stock", "product"],
    'assets': {
        'web.assets_backend': [
            'deliverysystem/static/src/js/delivery_route_map.js',
            'deliverysystem/static/src/js/plan_route.js',
            'deliverysystem/static/src/xml/delivery_route_map.xml',
        ],
    },
    'data': [
        "security/res_users_groups.xml",
        'security/ir.model.access.csv',
        "security/res_users_rules.xml",
        "views/delivery_parcel_views.xml",
        'views/block_scheduling_views.xml',
        'views/templates.xml',
        'views/res_config_settings_views.xml',
        'views/deliverysystem_config_menu.xml',
        'views/tracking_template.xml',
    ],
    "installable": True,
    "application": True,
    'demo': [
        'demo/demo.xml',
    ],
}

