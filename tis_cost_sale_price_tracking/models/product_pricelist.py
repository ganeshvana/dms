# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import fields, models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[('lot_with_cost', 'Lot with cost'),
                       ('lot_with_cost_and_landed_cost', 'Lot with Cost and Landed Cost')], ondelete={'lot_with_cost': 'cascade', 'lot_with_cost_and_landed_cost': 'cascade'})
