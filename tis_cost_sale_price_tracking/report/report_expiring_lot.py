# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import models, api
from datetime import datetime


class ReportTimesheet(models.AbstractModel):
    _name = 'report.tis_cost_sale_price_tracking.report_expiring_lot'

    @api.model
    def _get_report_values(self, docids, data=None):
        """we are overwriting this function because we need to show values from other models in the report
        we pass the objects in the docargs dictionary"""
        expiry_docs = self.env['lot.expiry'].browse(self.env.context.get('active_id'))
        docs = self.env['stock.production.lot'].search(
            [('removal_date', '>=', datetime.now()), ('removal_date', '<=', expiry_docs.compute_date())])
        return {
            'docs': docs,
            'expire_on': data.get('expire_on'),
            'delay_unit': data.get('delay_unit')
        }
