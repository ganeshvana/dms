# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import models, fields, api


class ReportBarcode(models.AbstractModel):
    _name = 'report.tis_cost_sale_price_tracking.report_lot_barcode'

    @api.model
    def _get_report_values(self, docids, data=None):
        """we are overwriting this function because we need to show values from other models in the report
        we pass the objects in the docargs dictionary"""
        datas = []
        docs = self.env['lot.barcode.wizard'].browse(int(data.get('active')))
        for data in data.get('datas'):
            datas.append(self.env['stock.production.lot'].browse(data))
        return {
            'doc_ids': self.ids,
            'docs': docs,
            'datas': datas
        }
