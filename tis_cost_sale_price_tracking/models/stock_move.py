# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.


from odoo import models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity, reserved_quant)
        if vals and vals.get('lot_id') and self.sale_line_id.available_lot_id:
            vals.update({'lot_id': self.sale_line_id.available_lot_id.id})
        return vals
