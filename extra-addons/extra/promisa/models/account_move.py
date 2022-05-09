# coding: utf-8
from odoo import fields, models, api
from num2words import num2words

class invoiceFields(models.Model):
    _inherit = 'account.move'

    po_num = fields.Char(string='P.O. Number', compute='_compute_po_num')
    amount_words = fields.Char('Amount in Words:',compute='_compute_num2words')

    def _compute_num2words(self):
        for record in self:
            if record.company_id.id == 2:
                try:
                    record.amount_words = (
                        num2words(record.amount_total, lang='en') + ' ' +
                        (record.currency_id.name or '')).upper()
                except NotImplementedError:
                    record.amount_words = (
                        num2words(record.amount_total, lang='en') + ' ' +
                        (record.currency_id.name or '')).upper()
            elif record.company_id.id == 1:
                try:
                    record.amount_words = (
                        num2words(record.amount_total, lang='es') + ' ' +
                        (record.currency_id.name or '')).upper()
                except NotImplementedError:
                    record.amount_words = (
                        num2words(record.amount_total, lang='es') + ' ' +
                        (record.currency_id.name or '')).upper()

    def _compute_po_num(self):
        for record in self:
            src_so = self.env['sale.order'].search([('name','=',record.invoice_origin)], limit=1)

            if len(src_so) > 0:
                record.po_num = src_so.po_num
            else:
                record.po_num = ''