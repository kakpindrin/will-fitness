# -*- coding: utf-8 -*-

from random import choice
from string import digits
from odoo import api, fields, models, _

class account_move(models.Model):
    _inherit = 'account.move'


    def action_register_payment(self):
        state_of_payment = ['paid', 'in_payment']
        if self.payment_state in state_of_payment:
            the_cards_domain = [('contact_id','=',self.partner_id.id)]
            the_all_cards = self.env['hr.rfid.card'].search(the_cards_domain, order='id desc')

            if len(the_all_cards) > 0:
                the_all_cards[0].write({
                    'deactivate_on': the_all_cards[0].activation_temp_date
                })
        result = super(account_move, self).action_register_payment()
        

        return result