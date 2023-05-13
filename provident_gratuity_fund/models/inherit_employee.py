# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ProvidentFundRuleConfig(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date('Joining Date', store=True)
    pf_account_id = fields.Many2one('account.account', 'PF Account')

    def pf_account_create(self):
        data = self.env['hr.employee'].search([])
        for rec in data:
            if (not rec.pf_account_id) and rec.joining_date and (date.today() - rec.joining_date).days > 180:
                emp = self.env['account.account'].search([('employee_id', '=', rec.id)])
                if not emp:
                    self.env['account.account'].create({
                        'name': rec.name + ' pf acc',
                        'code': rec.name + 'PA',
                        'user_type_id': 9,
                        'employee_id': rec.id,
                    })

                    acc = self.env['account.account'].search([('employee_id', '=', rec.id)])
                    rec.pf_account_id = acc.id


