# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import models


class LandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def button_validate(self):
        res = super(LandedCost, self).button_validate()
        for lines in self.valuation_adjustment_lines:
            for line in lines.move_id.move_line_ids:
                line.lot_id.landed_cost += lines.additional_landed_cost
        return res
