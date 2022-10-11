# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import api, models


class MrpStockReport(models.TransientModel):
    _inherit = 'stock.traceability.report'

    def _make_dict_move(self, level, parent_id, move_line, unfoldable=False):
        res = super(MrpStockReport, self)._make_dict_move(level, parent_id, move_line, unfoldable)
        for item in res:
            item['cost_price'] = move_line.lot_id.cost_price
            item['sale_price'] = move_line.lot_id.sale_price
            item['landed_cost'] = move_line.lot_id.landed_cost
        return res

    @api.model
    def _final_vals_to_lines(self, final_vals, level):
        lines = super(MrpStockReport, self)._final_vals_to_lines(final_vals, level)
        n = 0
        for item in final_vals:
            lines[n]['columns'].append(item.get('cost_price', 0.0))
            lines[n]['columns'].append(item.get('sale_price', 0.0))
            lines[n]['columns'].append(item.get('landed_cost', 0.0))
            n += 1
        return lines
