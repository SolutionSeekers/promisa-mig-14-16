# coding: utf-8
from odoo import fields, models, api
from num2words import num2words
from odoo.exceptions import UserError

class pickingFields(models.Model):
    _inherit = 'stock.picking'

    po_num = fields.Char(string='P.O. Number', compute='_compute_po_num')

    def _compute_po_num(self):
        for record in self:
            src_so = self.env['sale.order'].search([('name','=',record.origin)], limit=1)

            if len(src_so) > 0:
                record.po_num = src_so.po_num
            else:
                record.po_num = ''