# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class PFMainAccount(models.Model):
    _name = 'pf.main.account'
    _description = 'Employee PF Account'
    _rec_name = 'main_account_name'

    main_account = fields.Many2one('account.account', 'PF Main Account',ondelete='cascade')
    main_account_name = fields.Char('Name')
    main_account_code = fields.Char('Code')
    main_account_internal_type = fields.Char('Account Type')
    pf_lines = fields.One2many('employee.pf.account', 'main_id', 'Employee Account Lines',ondelete='cascade')

    @api.onchange('main_account')
    def _main_account_details(self):
        if self.main_account:
            self.main_account_name = self.main_account.name
            self.main_account_code = self.main_account.code
            self.main_account_internal_type = self.main_account.internal_type

    def compute_sheet(self):
        for rec in self.pf_lines:
            employee_acc = self.env['pfd.monthly.line'].search([('employee', '=', rec.employee.id)])
            pf = 0
            for val in employee_acc:
                pf += val.total_balance
            rec.pf_amount = pf



class EmployeePFAccount(models.Model):
    _name = 'employee.pf.account'
    _description = 'Employee PF Account'

    main_id = fields.Many2one('pf.main.account', 'Main Account', ondelete='cascade')
    employee = fields.Many2one('hr.employee', 'Employee', ondelete='cascade')
    employee_designation = fields.Char('Designation', store=True)
    employee_salary = fields.Float('Salary', store=True)
    employer_contribution_current = fields.Float('Employer Contribution Current', store=True, default=0.0)
    employer_contribution_previous = fields.Float('Employer Contribution Previous', store=True, default=0.0)
    pf_amount = fields.Float('PF Balance', store=True, default=0.0)
    join_date = fields.Date('Joining Date')
    pf_start_date = fields.Date('PF Start Date')

