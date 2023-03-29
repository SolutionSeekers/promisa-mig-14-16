
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class ActualizarPolizas(models.TransientModel):
    _name = 'actualizar.polizas'
    
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    polizas_de_facturas_de_cliente = fields.Boolean('Polizas de facturas de cliente')
    polizas_de_facturas_de_proveedor = fields.Boolean('Polizas de facturas de proveedor')
    polizas_de_facturas_de_pagos = fields.Boolean('Polizas de facturas de pagos')
    polizas_de_inventarios = fields.Boolean('Polizas de inventarios')
    polizas_de_micelaneos = fields.Boolean('Polizas de micelaneos')

    def action_validar_actualizar_polizas(self):
        if self.polizas_de_facturas_de_cliente:
            invoices = self.env['account.move'].search([('invoice_date','>=',self.fecha_inicio),
                                                           ('invoice_date','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['posted']),
                                                           ('type', '=', 'out_invoice')])
#            moves = invoices.mapped('id')
#            if moves:
#                moves.mapped('line_ids').write({'contabilidad_electronica':True})
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                inv.write({'contabilidad_electronica':True})
#                move_lines = inv.move_id.line_ids.filtered(lambda x:x.name=='')
#                for line in move_lines:
#                    cfdi_data = {'fecha': inv.invoice_date, 
#                                 'folio': inv.folio, 
#                                 'uuid': inv.folio_fiscal, 
#                                 'partner_id': inv.partner_id.id, 
#                                 'monto': inv.amount_total, 
#                                 'moneda': inv.moneda, 
#                                 'tipocamb': inv.tipocambio, 
#                                 'rfc_cliente': inv.partner_id.vat
#                                }
#                    if line.account_cfdi_ids:
#                        #Here, we are going to assume that move line will have only one cfdi line always
#                        line.account_cfdi_ids[0].write(cfdi_data)
#                    else:
#                        cfdi_data['move_line_id'] = line.id
#                        cfdi_obj.create(cfdi_data)


        if self.polizas_de_facturas_de_proveedor:
            invoices = self.env['account.move'].search([('invoice_date','>=',self.fecha_inicio),
                                                           ('invoice_date','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['posted']),
                                                           ('type', '=', 'in_invoice')])
            
#            moves = invoices.mapped('id')
#            if moves:
#                moves.mapped('line_ids').write({'contabilidad_electronica':True})
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                inv.write({'contabilidad_electronica':True})
                #move = inv.move_id
#                move_lines = inv.move_id.line_ids.filtered(lambda x:x.name=='/')
                #if move:
#                for line in move_lines:
#                    cfdi_data = {'fecha': inv.invoice_date, 
#                                 'folio': inv.folio, 
#                                 'uuid': inv.folio_fiscal, 
#                                 'partner_id': inv.partner_id.id, 
#                                 'monto': inv.amount_total, 
#                                 'moneda': inv.moneda, 
#                                 'tipocamb': inv.tipocambio, 
#                                 'rfc_cliente': inv.partner_id.vat
#                                 }
#                    if line.account_cfdi_ids:
#                        line.account_cfdi_ids[0].write(cfdi_data)
#                    else:
#                        cfdi_data['move_line_id'] = line.id
#                        cfdi_obj.create(cfdi_data)


        if self.polizas_de_facturas_de_pagos:
             #payments
             payments = self.env['account.payment'].search([('payment_date','>=',self.fecha_inicio),
                                                            ('payment_date','<=', self.fecha_fin),
                                                            ('estado_pago','=','pago_correcto'),
                                                            ('state','not in', ['draft', 'cancelled'])
                                                            ])

            # utilizado antes para habilitar la contabilidad electrónica en move lines
             #move_lines = payments.mapped('move_line_ids')
             #for move in payments.move_line_ids:
             #    _logger.info("move %s", move)
                 #move.write({'contabilidad_electronica':True})
                 #move_lines.mapped('move_id').write({'contabilidad_electronica':True})

             #antes para pasar la información de la factura a la póliza (ahora lo mismo) revisar para poner
             #cfdi_obj = self.env['account.move.cfdi33']
             #for payment in payments:
             #    for move in payment.move_line_ids.mapped('move_id'):
             #        cfdi_obj.create({'move_id': move.id,'fecha': payment.fecha_pago, 'folio': payment.name, 'uuid': payment.folio_fiscal, 'partner_id': payment.partner_id.id,
             #                         'monto': payment.amount, 'moneda': inv.moneda, 'tipocamb': inv.tipocambio, 'rfc_cliente': inv.partner_id.rfc})

             #effectively paid
             for payment in payments:
                   payment.diot = True
                  # _logger.info("move name %s", payment.move_name)
                   effective_pay = self.env['account.move'].search([('ref','=',payment.move_name), ('state','=', 'posted')],limit=1)
                   if effective_pay:
                      effective_pay.write({'contabilidad_electronica':True})
                      move_lines = effective_pay.line_ids
                   move_pay = self.env['account.move'].search([('name','=',payment.move_name), ('state','=', 'posted')],limit=1)
                   if move_pay:
                      move_pay.write({'contabilidad_electronica':True})

        if self.polizas_de_micelaneos:
            moves = self.env['account.move'].search([('date','>=',self.fecha_inicio),
                                             ('date','<=', self.fecha_fin),
                                             ('state','=', 'posted'),
                                             ('journal_id.type','=','general'),
                                             ])
            for move in moves:
                move.write({'contabilidad_electronica':True})

        return True
