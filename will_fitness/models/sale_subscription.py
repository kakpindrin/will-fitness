# -*- coding: utf-8 -*-

from random import choice
from string import digits
from odoo import api, fields, models, _
from datetime import datetime, date

class sale_subscription(models.Model):
    _inherit = 'sale.subscription'

    mode_reglement = fields.Selection(string="Mode Règlement", selection=[('especes','ESPÈCES'),
                                                         ('cartebancaire','CARTE BANCAIRE'),
                                                         ('virement','VIREMENT'),
                                                         ('cheque','CHÈQUE')], default="especes",)
    
    # date_start = fields.Date(string='Date de début', default=lambda self: self._get_default_date())

    # @api.model
    # def _get_default_date(self):
    #     now = datetime.now()
    #     today = now.date()
    #     la_date = now.strftime("%m/%d/%Y")

    #     debut_date = "01/08/2021"
    #     begin_date = datetime.strptime(debut_date, "%d/%m/%Y").date()
    #     ma_date = begin_date.strftime("%m/%d/%Y")

    #     if today <= begin_date:
    #         return begin_date
    #     else:
    #         return today

    
    #New field
    #description_contrat = fields.Text(string='Description Contrat')
    
    #THINK GOOD
    @api.model
    def create(self, values):
        """
            Create a new record for a model sale_subscription
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
    
        result = super(sale_subscription, self).create(values)

        partners_domain = [('id','=',result.partner_id.id)]
        all_partners = self.env['res.partner'].search(partners_domain, order='id desc')

        if len(all_partners) > 0:
            #for partner in all_partners:
            if not all_partners[0].barcode:
                a_barcode = '041'+"".join(choice(digits) for i in range(9))
                all_partners[0].write({
                    'barcode': a_barcode
                })

        the_partners_domain = [('id','=',result.partner_id.id)]
        the_all_partners = self.env['res.partner'].search(the_partners_domain, order='id desc')
        if len(the_all_partners) > 0:
            now = datetime.now()
    
            rfid_card = dict(None or {
                'number': the_all_partners[0].barcode,
                'contact_id': the_all_partners[0].id,
                'cloud_card': False,
                'activation_temp_date': result.recurring_next_date,
                'activate_on': result.date_start,
                'deactivate_on': result.date_start,
                })
            self.env['hr.rfid.card'].sudo().create(rfid_card)
        # result.write({
        #     'description_contrat': result.description,
        #     'description': False
        # })

        return result
    
    #THANKS GOD
    # @api.onchange('recurring_next_date')
    # def _onchange_my_recurring_next_date(self):
    #     for thist in self:
    #         if thist.recurring_next_date:
    #             the_cards_domain = [('contact_id','=',thist.partner_id.id)]
    #             the_all_cards = self.env['hr.rfid.card'].search(the_cards_domain, order='id desc')

    #             if len(the_all_cards) > 0:
    #                 the_all_cards[0].write({
    #                     'activation_temp_date': thist.recurring_next_date,
    #             })

    def generate_recurring_invoice(self):
        result = super(sale_subscription, self).generate_recurring_invoice()
        the_cards_domain = [('contact_id','=',self.partner_id.id)]
        the_all_cards = self.env['hr.rfid.card'].search(the_cards_domain, order='id desc')

        now = datetime.now()
        today = now.date()
        
        debut_date = "01/08/2021"
        begin_date = datetime.strptime(debut_date, "%d/%m/%Y").date()
        
        la_faveur = 0
        if today < begin_date:
            la_faveur = begin_date - today

        self.write({
            'recurring_next_date': self.recurring_next_date + la_faveur
        })
        #ma_date = begin_date.strftime("%m/%d/%Y")

        if len(the_all_cards) > 0:
            the_all_cards[0].write({
            'activation_temp_date': self.recurring_next_date,
        })

        return result