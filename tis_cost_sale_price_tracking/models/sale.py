# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for line in self.order_line:
            if line.product_id.tracking:
                if not line.available_lot_id:
                    raise UserError(_('You need to supply a lot/serial number for %s.') % line.product_id.name)
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    available_lot_id = fields.Many2one('stock.production.lot', string="Available lots")

    @api.onchange('available_lot_id')
    def lot_id_change(self):
        if self.order_id.pricelist_id and self.order_id.partner_id and self.available_lot_id:
            context = self._context.copy()
            if context.get('lot_params'):
                context['lot_params'].update({'available_lot_id': self.available_lot_id})
            else:
                context['lot_params'] = {'available_lot_id': self.available_lot_id}
            context['params'] = {'available_lot_id': self.available_lot_id}
            self.env.context = context
            price = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(self.product_id), self.product_id.taxes_id, self.tax_id, self.company_id)
            self.update({'price_unit': price})

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        res = {}
        if self.product_uom_qty and self.product_id.tracking == 'serial':
            if float_compare(self.product_uom_qty, 1.0, precision_rounding=self.product_id.uom_id.rounding) != 0:
                message = _(
                    'You can only process 1.0 %s of products with unique serial number.') % self.product_id.uom_id.name
                res['warning'] = {'title': _('Warning'), 'message': message}
        return res
