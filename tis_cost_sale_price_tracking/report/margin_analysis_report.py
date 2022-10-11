# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.


from odoo import fields, models, tools


class MarginAnalysisReport(models.Model):
    _name = "margin.analysis.report"
    _description = "Margin Analysis Report"
    _auto = False

    sale_order_id = fields.Many2one('sale.order', 'Sale', readonly=True)
    untaxed_sale = fields.Float(string="Untaxed Sale Price", readonly=True)
    taxed_sale = fields.Float(string="Taxed Sale Price", readonly=True)
    untaxed_margin = fields.Float(string="Untaxed Margin", readonly=True)
    taxed_margin = fields.Float(string="Taxed Margin", readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    lot_id = fields.Many2one('stock.production.lot', 'lot', readonly=True)
    category_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    cost_price = fields.Float(string="Cost Price", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

    def _select(self):
        select_str = """
                SELECT 
                    min(so.id) as id,
                    so.id as sale_order_id,
                    sol.product_id as product_id,
                    sol.price_subtotal as untaxed_sale,
                    (sol.price_subtotal + sol.price_tax) as taxed_sale,
                    lot.id as lot_id,
                    sol.price_subtotal - (lot.cost_price * sol.product_uom_qty) as untaxed_margin,
                    (sol.price_subtotal + sol.price_tax) - (lot.cost_price * sol.product_uom_qty) as taxed_margin,
                    (lot.cost_price * sol.product_uom_qty) as cost_price,
                    t.categ_id as category_id,so.user_id as user_id,
                    t.uom_id as product_uom,
                    so.company_id as company_id,
                    so.team_id as team_id
        """
        return select_str

    def _from(self):
        from_str = """
                sale_order_line sol 
                    join sale_order so on (sol.order_id = so.id) 
                    join stock_production_lot lot on (sol.available_lot_id = lot.id)
                    join product_product p on (lot.product_id=p.id) 
                    join product_template t on (p.product_tmpl_id=t.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                so.id,
                sol.product_id,
                lot.id,
                lot.cost_price,
                sol.available_lot_id,
                so.user_id,
                lot.cost_price,
                t.categ_id,
                t.uom_id,
                so.company_id,
                so.team_id,
                sol.price_tax,
                sol.product_uom_qty,
                sol.price_subtotal
        """
        return group_by_str
