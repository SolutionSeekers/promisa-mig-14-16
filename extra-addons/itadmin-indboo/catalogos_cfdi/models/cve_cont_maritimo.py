# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveContMaritimo(models.Model):
    _name = 'cve.cont.maritimo'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
