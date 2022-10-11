# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        params = self._context.get('params')
        lot_id = params.get('available_lot_id') if params else False
        if not uom and self._context.get('uom'):
            uom = self.env['uom.uom'].browse(self._context['uom'])
        if not currency and self._context.get('currency'):
            currency = self.env['res.currency'].browse(self._context['currency'])
        if price_type == 'lot_with_cost':
            products = self.with_context(
                force_company=company and company.id or self._context.get('force_company', self.env.company.id)).sudo()
            prices = dict.fromkeys(self.ids, 0.0)
            for product in products:
                if lot_id:
                    prices[lot_id.product_id.id] = lot_id.cost_price
                if uom:
                    prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

                if currency:
                    prices[product.id] = product.currency_id._convert(
                        prices[product.id], currency, product.company_id, fields.Date.today())
            return prices
        elif price_type == 'lot_with_cost_and_landed_cost':
            products = self.with_context(
                force_company=company and company.id or self._context.get('force_company', self.env.company.id)).sudo()
            prices = dict.fromkeys(self.ids, 0.0)
            for product in products:
                if lot_id:
                    prices[lot_id.product_id.id] = lot_id.cost_price + lot_id.landed_cost
                if uom:
                    prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

                if currency:
                    prices[product.id] = product.currency_id._convert(
                        prices[product.id], currency, product.company_id, fields.Date.today())
                return prices
        else:
            return super(ProductProduct, self).price_compute(price_type, uom, currency, company)
