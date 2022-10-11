# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _action_done(self):
        for ml in self.filtered(lambda m: m.qty_done > 0):
            if ml.move_id.sale_line_id:
                ml.lot_id.sale_price = ml.move_id.sale_line_id.price_unit
        context = self._context.copy()
        values = {}
        val = []
        for ml in self:
            values[ml] = ml.move_id.purchase_line_id
            val.append(ml)
        if context.get('lot_params'):
            context['lot_params'].update({'purchase_line_id': values})
        else:
            context['lot_params'] = {'purchase_line_id': values}
        self.env.context = context
        super(StockMoveLine, self)._action_done()
        for data in val:
            if data.id in self.search([]).ids:
                if data.lot_id:
                    if data.move_id.purchase_line_id:
                        if data.lot_id.product_id.tracking == 'lot':
                            data.lot_id._product_qty()
            if self._context.get('lot_params'):
                self._context.get('lot_params').pop('purchase_line_id')
