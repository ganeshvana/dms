# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import fields, models


class EncryptedCode(models.Model):
    _name = 'encrypted.code'

    name = fields.Char(default='Numeric Code')
    code_for_zero = fields.Char(string=' 0 ', required=True, limit=1, size=1,
                                help="add encrypted code for 0")
    code_for_one = fields.Char(string='1 ', required=True, limit=1, size=1,
                               help="add encrypted code for 1 ")
    code_for_two = fields.Char(string='2 ', required=True, limit=1, size=1,
                               help="add encrypted code for 2")
    code_for_three = fields.Char(string='3 ', required=True, limit=1, size=1,
                                 help="add encrypted code for 3")
    code_for_four = fields.Char(string='4 ', required=True, limit=1, size=1,
                                help="add encrypted code for 4")
    code_for_five = fields.Char(string='5 ', required=True, limit=1, size=1,
                                help="add encrypted code for 5")
    code_for_six = fields.Char(string='6 ', required=True, limit=1, size=1,
                               help="add encrypted code for 6")
    code_for_seven = fields.Char(string='7 ', required=True, limit=1, size=1,
                                 help="add encrypted code for 7 ")
    code_for_eight = fields.Char(string='8 ', required=True, limit=1, size=1,
                                 help="add encrypted code for 8 ")
    code_for_nine = fields.Char(string='9 ', required=True, limit=1, size=1,
                                help="add encrypted code for 9 ")
