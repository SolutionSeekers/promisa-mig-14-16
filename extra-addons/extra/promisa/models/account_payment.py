# coding: utf-8
from odoo import fields, models, api
from odoo.exceptions import UserError


class paymentRegisterFields(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.depends('can_edit_wizard')
    def _compute_communication(self):
        # The communication can't be computed in '_compute_from_lines' because
        # it's a compute editable field and then, should be computed in a separated method.
        for wizard in self:
            if wizard.can_edit_wizard:
                batches = wizard._get_batches()
                communication = ''
                # raise UserError(len(batches))
                for x in batches:
                    communication += ' ' + wizard._get_batch_communication(x)
                wizard.communication = communication
            else:
                wizard.communication = False

    @api.model
    def _get_batch_communication(self, batch_result):
        ''' Helper to compute the communication based on the batch.
        :param batch_result:    A batch returned by '_get_batches'.
        :return:                A string representing a communication to be set on payment.
        '''
        # raise UserError('batch_result: %s' % batch_result)
        labels = set(
            line.name or line.move_id.ref or line.move_id.name for line in batch_result['lines'])
        return ' '.join(sorted(labels))

    def _get_batches(self):
        ''' Group the account.move.line linked to the wizard together.
        :return: A list of batches, each one containing:
            * key_values:   The key as a dictionary used to group the journal items together.
            * moves:        An account.move recordset.
        '''
        # self.ensure_one()

        lines = self.line_ids._origin
        # raise UserError('lines: %s' % lines)
        # if len(lines.company_id) > 1:
        #     raise UserError(_("You can't create payments for entries belonging to different companies."))
        if not lines:
            raise UserError(
                _("You can't open the register payment wizard without at least one receivable/payable line."))

        batches = {}
        for line in lines:
            batch_key = self._get_line_batch_key(line)

            serialized_key = '-'.join(str(v) for v in batch_key.values())
            batches.setdefault(serialized_key, {
                'key_values': batch_key,
                'lines': self.env['account.move.line'],
            })
            batches[serialized_key]['lines'] += line
        # raise UserError('batches: %s' % list(batches.values()))
        return list(batches.values())

    @api.depends('line_ids')
    def _compute_from_lines(self):
        ''' Load initial values from the account.moves passed through the context. '''
        for wizard in self:
            batches = wizard._get_batches()
            batch_result = []
            # raise UserError('batches: %s' % batches)
            for elem in batches:
                batch_result.append(elem)
            wizard_values_from_batch = wizard._get_wizard_values_from_batch(
                batch_result)
            # raise UserError('wizard_values_from_batch: %s' %
            #                 wizard_values_from_batch)
            if len(batches) == 1:
                # == Single batch to be mounted on the view ==
                wizard.update(wizard_values_from_batch)

                wizard.can_edit_wizard = True
                wizard.can_group_payments = len(batch_result[0]['lines']) != 1
            else:
                # == Multiple batches: The wizard is not editable  ==
                wizard.update(wizard_values_from_batch)

                wizard.can_edit_wizard = True
                wizard.can_group_payments = len(batch_result[0]['lines']) != 1

    @api.model
    def _get_wizard_values_from_batch(self, batch_result):
        ''' Extract values from the batch passed as parameter (see '_get_batches')
        to be mounted in the wizard view.
        :param batch_result:    A batch returned by '_get_batches'.
        :return:                A dictionary containing valid fields
        '''
        source_amount = 0.0
        for elem in batch_result:
            key_values = elem['key_values']
            lines = elem['lines']
            company = lines[0].company_id

            source_amount += abs(sum(lines.mapped('amount_residual')))
            if key_values['currency_id'] == company.currency_id.id:
                source_amount_currency = source_amount
            else:
                source_amount_currency = abs(
                    sum(lines.mapped('amount_residual_currency')))

        return {
            'company_id': company.id,
            'partner_id': key_values['partner_id'],
            'partner_type': key_values['partner_type'],
            'payment_type': key_values['payment_type'],
            'source_currency_id': key_values['currency_id'],
            'source_amount': source_amount,
            'source_amount_currency': source_amount_currency,
        }
