# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import api, fields, models, _


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    cost_price = fields.Float(string='MRP Price', readonly=True)
    sale_price = fields.Float(string='Sale Price', readonly=True)
    landed_cost = fields.Float(string='Landed Cost', readonly=True)
    remaining_qty = fields.Float('Remaining Quantity', compute='_product_qty', store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductionLot, self).create(vals_list)
        lot_params = self._context.get('lot_params', False)
        if lot_params and lot_params.get('purchase_line_id', False):
            for ml in lot_params.get('purchase_line_id'):
                if ml.product_id == res.product_id and ml.lot_name == res.name:
                    res.cost_price = lot_params.get('purchase_line_id')[ml].price_unit
        return res

    def _product_qty(self):
        super(ProductionLot, self)._product_qty()
        for lot in self:
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
            lot.remaining_qty = lot.product_qty - (sum(quants.mapped('reserved_quantity')))

    def get_cost_in_code(self, cost_price):
        code = self.env['encrypted.code'].search([])[-1]
        if code:
            real = str(cost_price).split('.')[0]
            for i in real:
                if i == '0':
                    real = real.replace('0', code.code_for_zero)
                elif i == '1':
                    real = real.replace('1', code.code_for_one)
                elif i == '2':
                    real = real.replace('2', code.code_for_two)
                elif i == '3':
                    real = real.replace('3', code.code_for_three)
                elif i == '4':
                    real = real.replace('4', code.code_for_four)
                elif i == '5':
                    real = real.replace('5', code.code_for_five)
                elif i == '6':
                    real = real.replace('6', code.code_for_six)
                elif i == '7':
                    real = real.replace('7', code.code_for_seven)
                elif i == '8':
                    real = real.replace('8', code.code_for_eight)
                else:
                    real = real.replace('9', code.code_for_nine)
            return real
        else:
            return " "
