# coding: utf-8
from odoo import fields, models, api

class TreatmentCertificate(models.Model):
    _name = 'treatment.certificate'
    _description = 'Treatment Certificate'

    name = fields.Char(string="Folio", readonly=True, required=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner','Customer', default=lambda self: self.env.user.partner_id)
    line = fields.Char(string='Línea', required=True, store=True)
    note = fields.Text(string='Notas', store=True)
    medida_fito = fields.Char(string='Medida fitosanitaria', store=True)
    num_tipo_embalaje = fields.Char(string="Número de piezas y tipo de embalaje", store=True)
    volumen = fields.Integer(string='Volumen en metros cúbicos', store=True)
    application_date = fields.Date(string='Fecha de aplicación', store=True)
    treatment_start = fields.Datetime(string='Inicio de tratamiento', store=True)
    treatment_reach = fields.Datetime(string='Parametros alcanzados', store=True)
    treatment_end = fields.Datetime(string='Termino de tratamiento', store=True)
    tipo_madera = fields.Selection([
        ('conifera', 'CONIFERA'),
        ('noconifera', 'NO CONIFERA'),
        ('reconstruido', 'RECONSTRUIDO'),
    ], string='Tipo de madera', readonly=False)
    tipo_embalaje = fields.Selection([
        ('nuevo', 'NUEVO'),
        ('usado', 'USADO'),
        ('reconstruido', 'RECONSTRUIDO'),
    ], string='Tipo de embalaje', readonly=False)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'treatment.certificate') or 'New'
        result = super(TreatmentCertificate, self).create(vals)
        return result