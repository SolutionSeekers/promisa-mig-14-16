# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    total_imss = fields.Float(string='Total IMSS')

    def calculo_imss(self):
       res = super(HrPayslip, self).calculo_imss()
       for rec in self:
          rec.total_imss = self.pat_cuota_fija_pat + self.pat_exedente_smg + self.pat_prest_dinero + self.pat_esp_pens + self.pat_riesgo_trabajo + self.pat_invalidez_vida + self.pat_guarderias + self.pat_retiro + self.pat_cesantia_vejez + self.pat_infonavit
          rec.pat_total = self.pat_cuota_fija_pat + self.pat_exedente_smg + self.pat_prest_dinero + self.pat_esp_pens + self.pat_invalidez_vida + self.pat_cesantia_vejez
       return res