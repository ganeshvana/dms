# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	secondary_uom_id = fields.Many2one('uom.uom', string="Secondary UOM", compute='_compute_product_secondary_uom_qty', store=True)
	secondary_quantity = fields.Float('Secondary Qty',digits='Product Unit of Measure', compute='_compute_product_secondary_uom_qty', store=True)


	@api.depends('product_uom', 'product_uom_qty', 'product_id.uom_id')
	def _compute_product_secondary_uom_qty(self):
		for line in self:
			if line.product_id and line.product_id.uom_id and line.product_id.is_secondary_uom:
				line.secondary_quantity = line.product_id.uom_id._compute_quantity(line.product_uom_qty, line.product_id.secondary_uom_id)
				line.secondary_uom_id = line.product_id.secondary_uom_id.id
			else:
				line.secondary_quantity = 0.0
				line.secondary_uom_id = False
