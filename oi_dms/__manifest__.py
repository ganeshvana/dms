# -*- coding: utf-8 -*-

{
    'name': 'Menu',
    'category': 'Menu',
    'summary': 'Basic Menu form',
    'version': '15.0',
    'author': 'oodu implementers ',
    'description': """""",
    'depends': ['base', 'sale', 'stock', 'purchase', 'account', 'purchase_discount', 'product', 'coupon'],
    'application': True,
    'data': [
        'views/sale_inherit_view.xml',
        'views/inherit.xml',
        'security/ir.model.access.csv',


       
    ],
}
