# coding: utf-8
from odoo import fields, models, api
from num2words import num2words
from odoo.exceptions import UserError

class saleOrderFields(models.Model):
    _inherit = 'sale.order'

    po_num = fields.Char(string='P.O. Number')