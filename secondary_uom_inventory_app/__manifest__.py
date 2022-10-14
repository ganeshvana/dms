# -*- coding: utf-8 -*-

{
    'name' : "Inventory Secondary Unit of Measure-UOM",
    "author": "Edge Technologies",
    'version': '15.0.1.0',
    'live_test_url': "https://youtu.be/hmzRJ-4WE0k",
    "images":['static/description/main_screenshot.png'],
    'summary': 'Inventory secondary unit of measure for inventory secondary unit of measure for warehouse secondary unit of measure product secondary uom inventory secondary uom for warehouse secondary uom product secondary unit of measure for picking secondary uom',
    'description' : '''
           Inventory Secondary Unit of Measure.
    
secondary uom
Stock in Different UOMs
uom
Unit of Measure

    ''',
    "license" : "OPL-1",
    'depends' : ['stock', 'sale', 'purchase'],
    'data': [
            'security/ir.model.access.csv',
            'security/secondary_uom_group.xml',
            'views/account_invoice_view.xml',
            'views/product_view.xml',
            'views/stock_move_view.xml',
            'views/stock_inventory_view.xml',
            'views/stock_quant_view.xml',
            'views/stock_scrap_view.xml',
            'views/sale_order_view.xml',
            'views/purchase_order_view.xml',
            'views/inventory_report_template.xml',

             ],
    'installable': True,
    'auto_install': False,
    'price': 15,
    'currency': "EUR",
    'category': 'Warehouse',
}



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
