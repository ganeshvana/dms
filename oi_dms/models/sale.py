from odoo import api, fields, models, tools, _

class AreaName(models.Model):
    _name = "area"
    _description = "Area"

    name = fields.Char(string="Area Name", copy=False)
    area_code = fields.Char(string="Area Code", copy=False)
    company_ids = fields.Many2many("res.company", 'company_area_rel', 'company_id', 'area_id',string="Companies")

class BrandName(models.Model):
    _name = "brand"
    _description = "Brand"

    name = fields.Char(string="Brand Name", copy=False)
    brand_code = fields.Char(string="Brand Code", copy=False) 
    company_ids = fields.Many2many("res.company", 'company_brand_rel', 'company_id', 'brand_id',string="Companies")


class Division(models.Model):
    _name = "division"
    _description = "Division"

    name = fields.Many2one('res.partner', string="Division Name", copy=False)
    code = fields.Char(related="name.division_code", string="Division Code", copy=False)
    company_ids = fields.Many2many("res.company", 'company_division_rel', 'company_id', 'division_id',string="Companies")

class DivisionMenu(models.Model):
    _name = "division.menus"
    _description = "Division"

    name = fields.Many2one('res.partner', string="Division Name", copy=False)
    code_no = fields.Many2one('res.partner',string="Division Code", copy=False)
    company_ids = fields.Many2many("res.company", 'company_division_menus_rel', 'company_id', 'division_id',string="Companies")

class SubBrand(models.Model):
    _name = "sub.brand"
    _description = "Sub Brand"

    name = fields.Char(string="Sub Brand Name", copy=False)
    subbrand_code = fields.Char(string="Sub Brand Code", copy=False)
    company_ids = fields.Many2many("res.company", 'company_sb_rel', 'company_id', 'sb_id',string="Companies")


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = "Res Company"

    area = fields.Many2many('area', string="Area Name ", copy=False)
    division_ids = fields.Many2many('res.partner','company_disibuor_rel','disibutor_id','company_id',  string="Division", copy=False)
    division_brand_ids = fields.Many2many('brand', 'distributor_brand_rel', 'company_id', 'brand_id', "Division Brand")
    division_subbrand_ids = fields.Many2many('sub.brand', 'distributor_subbrand_rel', 'company_id', 'subrand_id', "Division Sub Brand")
    distributor_code = fields.Char(string="Distributor Code", copy=False)
    brand = fields.Many2many('brand', string="Brand", copy=False)
    sub_brand = fields.Many2many('sub.brand', string="Sub-Brand", copy=False)
    pan = fields.Char("Pan")
    state_code = fields.Char(related='state_id.code')
    value = fields.Char("")
    
    @api.onchange('division_ids')
    def onchange_division_ids(self):
        brand = subbrand = []
        result = {}
        if self.division_ids:
            for divi in self.division_ids:
                if divi.brand_id:
                    for br in divi.brand_id:
                        brand.append(br.id)
        self.division_brand_ids = [(6,0, brand)] 
        if self.division_ids: 
            subbrand = []           
            for div in self.division_ids:  
                if div.subbrand_id:
                    for sbr in div.subbrand_id:
                        subbrand.append(sbr.id)  
        # self.distributor_code =  subbrand     
        self.division_subbrand_ids = [(6,0, subbrand)]    
        # self.sub_brand = [(6, 0, subbrand)]
        # if self.division_ids:
        #     br_list = sbr_list = []
        #     for rec in self.division_ids:
        #     if self.brand and self.sub_brand:
        #         for b in self.brand:
        #             if b in 

class ProductTemplate(models.Model):
    _inherit = "product.template"

    division_id = fields.Many2one('res.partner', string="Division", copy=False)
    brand_id = fields.Many2one('brand',string="Brand", copy=False)
    subbrand_id = fields.Many2one('sub.brand',string="Sub Brand", copy=False)
    no_of_pcs = fields.Char(string="No.of pcs in Packet", copy=False)
    mrp = fields.Float(string="MRP", copy=False)
    division_brand_ids = fields.Many2many('brand', 'product_brand_rel', 'company_id', 'brand_id', "Division Brand")
    division_subbrand_ids = fields.Many2many('sub.brand', 'product_subbrand_rel', 'company_id', 'subrand_id', "Division Sub Brand")
    tax_structure_ids = fields.One2many('product.tax.structure', 'product_template_id', "Tax Structure")
    
    
    @api.onchange('division_id')
    def onchange_division_id(self):
        brand = subbrand = []
        result = {}
        if self.division_id:
            for divi in self.division_id:
                if divi.brand_id:
                    for br in divi.brand_id:
                        brand.append(br.id)
        self.division_brand_ids = [(6,0, brand)] 
        if self.division_id: 
            subbrand = []           
            for div in self.division_id:  
                if div.subbrand_id:
                    for sbr in div.subbrand_id:
                        subbrand.append(sbr.id)        
            
            result['domain'] = {
                    'subbrand_id': [('id', 'in', subbrand)]
                }
        if not self.division_id: 
            self.brand_id = False
            self.subbrand_id = False
        return result
        
    @api.onchange('division_id')
    def onchange_division_ids(self):
        subbrand = []
        if self.division_id:            
            for div in self.division_id:  
                if div.subbrand_id:
                    for sbr in div.subbrand_id:
                        subbrand.append(sbr.id)        
            self.division_subbrand_ids = [(6,0, subbrand)]  
        
        
class ProductTaxStructure(models.Model):
    _name = "product.tax.structure"
    _description = "Product Tax Structure"
    
    product_template_id = fields.Many2one('product.template')
    from_amount = fields.Float("From Amount")
    to_amount = fields.Float("To Amount")
    sale_tax_ids = fields.Many2many('account.tax', 'product_sale_tax_rel', 'tax_id', 'prod_str_id', string="Sale Taxes")
    purchase_tax_ids = fields.Many2many('account.tax', 'product_purchase_tax_rel', 'tax_id', 'prod_str_id', string="Purchase Taxes")

class ContactMaster(models.Model):
    _inherit = "res.partner"

    area = fields.Many2one('area', string="Area", copy=False)
    is_division = fields.Boolean(string="Is Division", copy=False)
    division_code = fields.Char(string="Division Code",copy=False,)
    brand_id = fields.Many2many('brand',string="Brand", copy=False)
    subbrand_id = fields.Many2many('sub.brand',string="Sub Brand", copy=False)
    res_line_ids = fields.One2many('res.partner.line', 'rp_id', string="Distributor")
    discount = fields.Float("Dealer Discount")

class ContactMaster(models.Model):
    _name = "res.partner.line"

    rp_id = fields.Many2one('res.partner',string='Partner')
    division_id = fields.Many2one('res.partner', string="Division", copy=False)
    distributor_id = fields.Many2one('res.company',string='Distributor')
    division_ids = fields.Many2many(related='distributor_id.division_ids')
    brand_ids = fields.Many2many('brand',string="Brand", copy=False)
    sub_brand_ids = fields.Many2many('sub.brand', string="Sub-Brand", copy=False)
    company_ids = fields.Many2many(related='rp_id.company_ids')    
    division_brand_ids = fields.Many2many('brand', 'partner_brand_rel', 'partner_id', 'brand_id', "Division Brand")
    division_subbrand_ids = fields.Many2many('sub.brand', 'partner_subbrand_rel', 'partner_id', 'subrand_id', "Division Sub Brand")
    price_list_id = fields.Many2one('product.pricelist', "Pricelist")
    promotion_id = fields.Many2one('coupon.program', "Promotion")
    
    @api.onchange('division_id')
    def onchange_division_id(self):
        brand = subbrand = []
        result = {}
        if self.division_id:
            for divi in self.division_id:
                if divi.brand_id:
                    for br in divi.brand_id:
                        brand.append(br.id)
        self.division_brand_ids = [(6,0, brand)] 
        if self.division_id: 
            subbrand = []           
            for div in self.division_id:  
                if div.subbrand_id:
                    for sbr in div.subbrand_id:
                        subbrand.append(sbr.id)        
        self.division_subbrand_ids = [(6,0, subbrand)] 
        #     result['domain'] = {
        #             'sub_brand_ids': [('id', 'in', subbrand)]
        #         }
        #
        # return result 
    
    
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    oop_ref_no = fields.Char('OOP Order No', copy=False)
    oop_order_date = fields.Date('OOP Order Date', copy=False)
    transport_name = fields.Char(string="Transport Name", copy=False) 
    mrp_name = fields.Char(string="MRP", copy=False)
    destination = fields.Char(string="Destination", copy=False)
    from_ramraj = fields.Boolean("From Ramraj")
    cancel = fields.Boolean("Cancel")
    
class StockPicking(models.Model):
    _inherit = "stock.picking"

    trans_name = fields.Char(related='purchase_id.transport_name',string="Transport Name",copy=False)
    ramraj_ref_no = fields.Char(string="Ramraj Ref NO", copy=False)
    ramraj_ref_date = fields.Date(string="Ramraj Ref date", copy=False)
    from_ramraj = fields.Boolean("From Ramraj")
    partial = fields.Boolean("Partial")
    backorder = fields.Boolean("Back Order")
    cancel = fields.Boolean("Cancel")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    oop_ref_no = fields.Char('OOP Order No', copy=False)
    oop_order_date = fields.Date('OOP Order Date', copy=False)
    mrp_name_no = fields.Char(string="MRP", copy=False)
    brand_id_name = fields.Many2one('brand',string="Brand", copy=False)
    subbrand_id_name = fields.Many2one('sub.brand',string="Sub Brand", copy=False)
    from_ramraj = fields.Boolean("From Ramraj")
    division_id = fields.Many2one('res.partner', string="Division", copy=False)
    
    @api.model
    def create(self, vals):
        res = super().create(vals)  
        if res.partner_id:
            if res.partner_id.res_line_ids:
                lines = res.partner_id.res_line_ids.filtered(lambda m: m.distributor_id == res.company_id and m.division_id == res.division_id)
                if lines:
                    res.pricelist_id = lines[0].price_list_id.id
                    res.update_prices()
        if res.from_ramraj == True:
            res.action_confirm()
        return res
    
class Accounting(models.Model):
    _inherit = "account.move.line"

    product_mrp = fields.Float(related='product_id.list_price',string="MRP", copy=False)
    
    
class Move(models.Model):
    _inherit = "account.move"
    
    @api.onchange('move_type')
    def onchange_move_type(self):
        if self.move_type:
            if self.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                partner = self.env['res.partner'].search([('customer_rank','>', 0)])
                return {'domain':{'partner_id': [('id', 'in', partner.ids)]}}
            if self.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
                partner = self.env['res.partner'].search(['|',('supplier_rank','>', 0),('is_division', '=', True)])
                return {'domain':{'partner_id': [('id', 'in', partner.ids)]}}

    
class PurchaseOrder(models.Model):
    _inherit = "purchase.order.line"   

    value_before_discount = fields.Float(string="Value before Discount", compute="_compute_value_before_discount", store=True)
    mrp = fields.Float(related='product_id.list_price', string="MRP",copy=False)
    discount_amount = fields.Float(compute="_compute_value_before_discount", store=True)
    unitprice_after_discount = fields.Float("Unit Price After Discount", compute='compute_unit_discount' , store=True)
    
    @api.onchange('unitprice_after_discount', 'price_unit', 'discount')
    def onchange_price_discount(self):
        if self.price_unit:
            if self.unitprice_after_discount:
                if self.product_id.tax_structure_ids:
                    taxline = self.product_id.tax_structure_ids.filtered(lambda m: self.unitprice_after_discount >= m.from_amount and self.unitprice_after_discount <= m.to_amount)
                    if taxline:
                        fpos = self.order_id.fiscal_position_id or self.order_id.fiscal_position_id.get_fiscal_position(self.order_partner_id.id)
                        self.taxes_id = fpos.map_tax(taxline.purchase_tax_ids)
                    else:
                        taxes = self.product_id.supplier_taxes_id.filtered(lambda t: t.company_id == self.env.company)
                        fpos = self.order_id.fiscal_position_id or self.order_id.fiscal_position_id.get_fiscal_position(self.order_partner_id.id)
                        self.taxes_id = fpos.map_tax(taxes)

    @api.depends('price_unit', 'discount')
    def compute_unit_discount(self):
        for rec in self:
            if rec.price_unit and rec.discount > 0:
                rec.unitprice_after_discount = rec.price_unit - (rec.price_unit * (rec.discount) /100)
            else:
                rec.unitprice_after_discount = rec.price_unit
    
    @api.depends('price_unit', 'product_uom_qty', 'discount', 'price_subtotal')
    def _compute_value_before_discount(self):
        for record in self:
            record.value_before_discount = record.price_unit * record.product_uom_qty
            if record.discount > 0:
                record.discount_amount = (record.price_unit * record.product_uom_qty) - record.price_subtotal
            else:
                record.discount_amount = 0.0

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"   

    value_before_discount = fields.Float(string="Value before Discount", compute="_compute_value_before_discount", store=True)
    mrp = fields.Float(related='product_id.list_price', string="MRP",copy=False)
    discount_amount = fields.Float(compute="_compute_value_before_discount", store=True)
    unitprice_after_discount = fields.Float("Unit Price After Discount", compute='compute_unit_discount' , store=True)
    
    @api.onchange('unitprice_after_discount', 'price_unit', 'discount')
    def onchange_price_discount(self):
        if self.price_unit:
            if self.unitprice_after_discount:
                if self.product_id.tax_structure_ids:
                    taxline = self.product_id.tax_structure_ids.filtered(lambda m: self.unitprice_after_discount >= m.from_amount and self.unitprice_after_discount <= m.to_amount)
                    if taxline:
                        fpos = self.order_id.fiscal_position_id or self.order_id.fiscal_position_id.get_fiscal_position(self.order_partner_id.id)
                        self.tax_id = fpos.map_tax(taxline.sale_tax_ids)
                    else:
                        taxes = self.product_id.taxes_id.filtered(lambda t: t.company_id == self.env.company)
                        fpos = self.order_id.fiscal_position_id or self.order_id.fiscal_position_id.get_fiscal_position(self.order_partner_id.id)
                        self.tax_id = fpos.map_tax(taxes)

    @api.depends('price_unit', 'discount')
    def compute_unit_discount(self):
        for rec in self:
            if rec.price_unit and rec.discount > 0:
                rec.unitprice_after_discount = rec.price_unit - (rec.price_unit * (rec.discount) /100)
            else:
                rec.unitprice_after_discount = rec.price_unit
    
    @api.depends('price_unit', 'product_uom_qty', 'discount', 'price_subtotal')
    def _compute_value_before_discount(self):
        for record in self:
            record.value_before_discount = record.price_unit * record.product_uom_qty
            if record.discount > 0:
                record.discount_amount = (record.price_unit * record.product_uom_qty) - record.price_subtotal
            else:
                record.discount_amount = 0.0
                
    def create(self, vals):        
        res = super().create(vals)
        res.discount = res.order_id.partner_id.discount
        return res
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.discount = self.partner_id.discount
   
class StockMoveInherited(models.Model):
    _inherit = "stock.move"

    transit_qty = fields.Float('Transit Qty', copy=False)
    transit_sec_qty = fields.Float('Transit Secondary Qty', copy=False)

