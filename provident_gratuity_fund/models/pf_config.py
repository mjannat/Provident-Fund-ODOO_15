# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class ProvidentFundRuleConfig(models.Model):
    _name = 'provident.fund.rule.config'
    _description = 'provident_fund.provident_fund'
    __rec_name = 'name'

    name = fields.Char('Rule Name', store=True)
    rule_date = fields.Date('Date', store=True)
    employee_contribution = fields.Float('Employee Contribution(%)', store=True)
    employer_contribution = fields.Float('Employer Contribution(%)', store=True)
    status = fields.Boolean('Status', store=True, default=False)

    @api.onchange('status')
    def status_active_checking(self):
        check = self.env['provident.fund.rule.config'].search([('status', '=', True)])
        print(check.id)
        if check.status and check.name != self.name:
            raise UserError(_('Another rules is active now'))
        else:
            prospect = self.env['hr.salary.rule'].search([('code', '=', 'PFD')])
            if prospect:
                prospect.update({
                    'amount_percentage': self.employee_contribution,
                })
            else:
                prospect.create({
                        'name': 'Provident Fund Deduction',
                        'code': 'PFD',
                        'category_id': 4,
                        'condition_select': 'none',
                        'amount_select': 'percentage',
                        'amount_percentage_base': 'categories.BASIC',
                        'quantity': 1.0,
                        'amount_percentage': self.employee_contribution * -1,
                    })

