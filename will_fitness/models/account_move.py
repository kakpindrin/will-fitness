# -*- coding: utf-8 -*-

from random import choice
from string import digits
from odoo import api, fields, models, _

class account_move(models.Model):
    _inherit = 'account.move'

    @api.multi
    def generate_recurring_invoice(self):
        result = super(account_move, self).action_register_payment()
        state_of_payment = ['paid', 'in_payment']
        if result.payment_state in state_of_payment:
            the_cards_domain = [('contact_id','=',result.partner_id.id)]
            the_all_cards = self.env['hr.rfid.card'].search(the_cards_domain, order='id desc')

            if len(the_all_cards) > 0:
                the_all_cards[0].write({
                    'deactivate_on': the_all_cards[0].activation_temp_date
                })

        return result

    # @api.onchange('payment_state')
    # def _onchange_payment_state(self):
    #     for thist in self:
    #         state_of_payment = ['paid', 'in_payment']
    #         if thist.payment_state in state_of_payment:
    #             the_cards_domain = [('contact_id','=',thist.partner_id.id)]
    #             the_all_cards = self.env['hr.rfid.card'].search(the_cards_domain, order='id desc')

    #             if len(the_all_cards) > 0:
    #                 the_all_cards[0].write({
    #                     'deactivate_on': the_all_cards[0].activation_temp_date
    #                 })