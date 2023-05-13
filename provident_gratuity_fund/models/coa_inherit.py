# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class AccountCOA(models.Model):
    _inherit = 'account.account'

    employee_id = fields.Many2one('hr.employee', store=True)
    # pf_account_id = fields.Many2one('account.account')