# coding: utf-8
from odoo import fields, models, api
from num2words import num2words
from odoo.exceptions import UserError


class productTemplateFields(models.Model):
    _inherit = 'product.template'

    x_cliente = fields.Many2one(string='Cliente', comodel_name='res.partner')
