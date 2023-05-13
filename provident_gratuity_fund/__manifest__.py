# -*- coding: utf-8 -*-
{
    'name': "Provident Fund & Gratuity Fund",

    'summary': """
        Provident Fund Module Integrated with payroll""",

    'description': """
        Provident Fund for Employees
    """,

    'author': "Mim Jannat",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'om_hr_payroll', 'account', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/pf_config.xml',
        'views/monthly_pfd_cal.xml',
        'views/employee_pf_acc_view.xml',
        'views/hr_employee_inherit.xml',
        'views/account_move_line_inherit_view.xml',
        'reports/provident_fund_monthly_details.xml',
        'data/cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
