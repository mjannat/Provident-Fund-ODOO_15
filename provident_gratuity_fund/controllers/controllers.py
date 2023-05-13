# -*- coding: utf-8 -*-
# from odoo import http


# class ProvidentFund(http.Controller):
#     @http.route('/provident_fund/provident_fund/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/provident_fund/provident_fund/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('provident_fund.listing', {
#             'root': '/provident_fund/provident_fund',
#             'objects': http.request.env['provident_fund.provident_fund'].search([]),
#         })

#     @http.route('/provident_fund/provident_fund/objects/<model("provident_fund.provident_fund"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('provident_fund.object', {
#             'object': obj
#         })
