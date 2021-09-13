# coding: utf-8
from odoo import fields, models, api


class addressFields(models.Model):
    _inherit = 'hr.employee'

    address_char = fields.Char(string="Dirección")
    locker_no = fields.Char(string="No. Locker")
