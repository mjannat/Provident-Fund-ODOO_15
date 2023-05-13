from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    hello_world = fields.Char('Hello World')
