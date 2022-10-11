# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from datetime import datetime
from odoo.exceptions import UserError
from odoo import fields, models, _
from dateutil.relativedelta import relativedelta


class LotExpiry(models.Model):
    _name = "lot.expiry"

    expire_on = fields.Integer("Expire On", default=1)
    delay_unit = fields.Selection([
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('months', 'months'),
        ('years', 'years'), ], string="Delay units", help="Unit of delay", required=True, default='days')

    def compute_date(self):
        if self.delay_unit == 'days':
            date_filter = datetime.now() + relativedelta(days=self.expire_on)
        elif self.delay_unit == 'weeks':
            date_filter = datetime.now() + relativedelta(weeks=self.expire_on)
        elif self.delay_unit == 'months':
            date_filter = datetime.now() + relativedelta(months=self.expire_on)
        else:
            date_filter = datetime.now() + relativedelta(years=self.expire_on)
        return date_filter

    def view_expire_lots(self):
        action = self.env.ref('stock.action_production_lot_form').read()[0]
        if not 'removal_date' in self.env['stock.production.lot']._fields:
            raise UserError(_('Activate Expiration Dates in Traceability settings'))
        action['domain'] = [('removal_date', '<=', self.compute_date()), ('removal_date', '>=', datetime.now())]
        return action

    def print_report(self):
        if not 'removal_date' in self.env['stock.production.lot']._fields:
            raise UserError(_('Activate Expiration Dates in Traceability settings'))
        data = {
            'expire_on': self.expire_on,
            'delay_unit': self.delay_unit
        }
        return self.env.ref('tis_cost_sale_price_tracking.action_report_print_expiring_lot').report_action(self,
                                                                                                           data=data)
