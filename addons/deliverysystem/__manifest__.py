# -*- coding: utf-8 -*-
{
    'name': "Delivery System",

    'summary': "Module to extend Odoo for delivery management",

    'description': """
Long description of module's purpose
    """,

    'author': "Osman Elsahib",
    'website': "https://www.dflex.co.uk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Delivery',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',"sale", "stock", "product"],

    # always loaded
    'data': [
        "security/res_users_groups.xml",
        'security/ir.model.access.csv',
        "security/res_users_rules.xml",
        "views/delivery_views.xml",
        'views/views.xml',
        'views/templates.xml',
        
    ],
    # only loaded in demonstration mode
    "installable": True,
    "application": True,
    'demo': [
        'demo/demo.xml',
    ],
}

