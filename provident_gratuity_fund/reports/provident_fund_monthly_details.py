from odoo import models


class ProvidentFundMonthlyReport(models.AbstractModel):
    _name = 'report.provident_fund.provident_fund_monthly_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Provident Fund Monthly Statement')
        format_heading = workbook.add_format({'valign': 'vcenter', 'font_size': 10, 'align': 'center', 'bold': True, 'border': True, 'font_name':'cambria'})
        format_heading_rotate = workbook.add_format({'font_size': 10,'valign': 'vcenter', 'align': 'center', 'bold': True,
                                                     'border': True, 'rotation': '90', 'text_wrap': True,'font_name':'cambria','bg_color':'#d9d1d1'})

        format_body = workbook.add_format({'font_size': 10,'valign': 'vcenter', 'align': 'center', 'border': True, 'font_name':'cambria'})
        format_body_name = workbook.add_format({'font_size': 10,'valign': 'vcenter', 'align': 'left', 'border': True, 'font_name':'cambria'})


        bold = workbook.add_format(
            {'font_size': 15, 'bold': True, 'align': 'center','valign': 'vcenter', 'border': True, 'font_name':'cambria'})

        sheet.set_column(1, 7, 20)

        row = 2
        serial_number = 1
        sheet.set_row(0, 40)
        col = 3

        sheet.merge_range('A1:H1', 'Monthly Provident Fund Summary Report', bold)

        sheet.write(1, 0, 'SI', format_heading)
        sheet.write(1, 1, 'Employee Name', format_heading)
        sheet.write(1, 2, 'Contribution Month', format_heading)
        sheet.write(1, 3, 'Contribution Year', format_heading)
        sheet.write(1, 4, 'Contribution Amount', format_heading)
        sheet.write(1, 5, 'Previous Balance', format_heading)
        sheet.write(1, 6, 'Total', format_heading)
        sheet.write(1, 7, 'Contribution Type', format_heading)

        for index, line in enumerate(lines):
            sheet.merge_range('A1:E1', line.month + ' Provident Fund Summary Report', bold)
            for ind, item in enumerate(line.pfd_line_ids):
                sheet.write(row, 0, serial_number, format_body)
                sheet.write(row, 1, 'PF of ' + item.employee.name, format_body)
                sheet.write(row, 2, item.pfd_main_id.month, format_body)
                sheet.write(row, 3, item.pfd_main_id.year, format_body)
                sheet.write(row, 4, item.current_month_tk, format_body)
                sheet.write(row, 5, item.previous_balance, format_body)
                sheet.write(row, 6, item.total_balance, format_body)
                sheet.write(row, 7, item.pfd_main_id.type, format_body)
                serial_number += 1
