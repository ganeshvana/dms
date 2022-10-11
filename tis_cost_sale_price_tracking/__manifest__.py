# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

{
    'name': 'Cost & Sale Price Tracking',
    'version': '15.0.0.1',
    'category': 'Inventory',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': 'http://www.technaureus.com/',
    'depends': ['sale_management', 'stock_landed_costs', 'tis_barcode_paperformat', 'product_expiry'],
    'summary': 'Sale and Purchase prodcuct tracking with lots',
    'description': """
    This module contains the features to track sale and purchase products with lots.
    Sales price based on cost price.
    """,
    'price': 35,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'data/setup_cost_price_code.xml',
        'security/ir.model.access.csv',
        'report/report_lot_barcode.xml',
        'views/barcode_generator_view.xml',
        'views/stock_production_lot_views.xml',
        'views/sale_views.xml',
        'report/margin_analysis_report_views.xml',
        'report/report_lot_barcode_template.xml',
        'report/report_expiring_lot.xml',
        'report/report_expiring_lot_template.xml',
        'wizard/barcode_lot_wizard_views.xml',
        'wizard/expire_lot_wizard_views.xml',
        'views/product_pricelist_views.xml',
        'views/report_stock_traceability.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
