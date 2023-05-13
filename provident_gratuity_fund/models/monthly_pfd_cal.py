# -*- coding:utf-8 -*-

import datetime as dt
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from pytz import timezone

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class MonthlyPFD(models.Model):
    _name = 'pfd.monthly.cal'
    _description = 'PFD Calculation Monthly'
    _rec_name = 'month'

    date_from = fields.Date(string='Date From', readonly=False, required=True,
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date(string='Date To', readonly=False, required=True,
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    month = fields.Char('Month', store=True)
    year = fields.Char('Year', store=True)
    type = fields.Char('Contribution Type', store=True)
    pfd_coa = fields.Float('COA PFD Balance', store=True)
    pfd_line_ids = fields.One2many('pfd.monthly.line', 'pfd_main_id', string='PFD Lines')

    @api.onchange('date_from', 'date_to')
    def _compute_balance(self):
        if self.date_from:
            date_val = self.date_from
            self.month = date_val.strftime("%B")
            self.year = date_val.strftime("%Y")

    def compute_sheet(self):
        if self.date_from and self.date_to:
            amount = self.env['hr.payslip'].search([('date_from', '=', self.date_from), ('date_to', '=', self.date_to), ('state', '=', 'done')])
            employer_contribution = self.env['provident.fund.rule.config'].search([('status', '=', True)])
            print("Amount:", amount)
            if not amount:
                raise UserError(_('There is no employee payroll on this period'))
            else:
                lines = [(5, 0, 0)]
                value = {}
                previous_balance = 0.0
                sum = 0.0
                for rec in amount:
                    print("employee:", rec.employee_id.id)
                    if rec.employee_id:
                        employee_acc = self.env['employee.pf.account'].search([('employee', '=', rec.employee_id.id)])
                        print("employee_ac:", employee_acc.pf_amount)
                        if employee_acc:
                            previous_balance = employee_acc.pf_amount
                            for res in rec.line_ids:
                                if res.salary_rule_id.code == 'PFD':
                                    print("Employee ID:", rec.employee_id.id)
                                    res.total = res.total * (-1)
                                    total = previous_balance + res.total + (res.total * float(employer_contribution.employer_contribution/100.00))
                                    value = {
                                        'employee': rec.employee_id.id,
                                        'current_month_tk': (res.total * 2) if res.total else 0.0,
                                        'employee_contribution': res.total if res.total else 0.0,
                                        'company_contribution': res.total if res.total else 0.0,
                                        'previous_balance': previous_balance,
                                        'employer_con_mon_current': res.total * (employer_contribution.employer_contribution/100.00),
                                        'total_balance': total + res.total,
                                    }
                                    sum += total
                                    lines.append((0, 0, value))
            self.pfd_line_ids = lines
            self.pfd_coa = sum


class MonthlyPFDLineItem(models.Model):
    _name = 'pfd.monthly.line'
    _description = 'PFD Monthly Deduction'

    pfd_main_id = fields.Many2one('pfd.monthly.cal', 'PFD ID', ondelete='cascade')
    employee = fields.Many2one('hr.employee', 'Employee', ondelete='cascade')
    current_month_tk = fields.Float('Current Month Amount', store=True)
    employee_contribution = fields.Float('Employee Contribution', store=True)
    company_contribution = fields.Float('Company Contribution', store=True)
    previous_balance = fields.Float('Previous Balance', store=True, default=0.0)
    total_balance = fields.Float('Total Balance')
    employer_con_mon_current = fields.Float('Employer Contribution Current', store=True, default=0.0)
    employer_con_total = fields.Float('Employer Contribution Total', store=True, default=0.0)

    @api.onchange('employee', 'current_month_tk')
    def _compute_current_month(self):
        for rec in self:
            if rec.current_month_tk:
                rec.employee_contribution = rec.current_month_tk
                rec.company_contribution = rec.current_month_tk
                rec.current_month_tk += rec.employee_contribution

            employee_acc = self.env['employee.pf.account'].search([('employee', '=', rec.employee.id)])
            if employee_acc:
                rec.previous_balance = employee_acc.pf_amount
                employee_acc.pf_amount += rec.current_month_tk
                employee_acc.main_id += rec.current_month_tk



