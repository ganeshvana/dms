# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import fields, models


class LotBarcodeWizard(models.TransientModel):
    _name = 'lot.barcode.wizard'

    show_price = fields.Boolean(string='Show Sale Price')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id, string="Currency")
    show_sale_price = fields.Boolean(string='Show Sale Price')
    show_cost_price = fields.Boolean(string='Show cost Price')
    including_landed_cost = fields.Boolean(string='Including Landed Cost', help='Cost Price including landed cost')

    def print_barcode(self):
        active_ids = self._context.get('active_ids')
        active_field = self.id
        return self.env.ref('tis_cost_sale_price_tracking.action_lot_barcode_sticker_report').report_action(self, data={
            'datas': active_ids, 'active': active_field})
