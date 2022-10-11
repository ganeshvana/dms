# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import models, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        res = super(StockQuant, self)._update_reserved_quantity(product_id, location_id,
                                                                quantity, lot_id=lot_id,
                                                                package_id=package_id, owner_id=owner_id,
                                                                strict=strict)
        for data in res:
            if data[0].lot_id:
                if data[0].lot_id.product_id.tracking == 'lot':
                    data[0].lot_id._product_qty()
        return res
