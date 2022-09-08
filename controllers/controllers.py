# -*- coding: utf-8 -*-
# from odoo import http


# class ControlAcceso(http.Controller):
#     @http.route('/control_acceso/control_acceso', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/control_acceso/control_acceso/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('control_acceso.listing', {
#             'root': '/control_acceso/control_acceso',
#             'objects': http.request.env['control_acceso.control_acceso'].search([]),
#         })

#     @http.route('/control_acceso/control_acceso/objects/<model("control_acceso.control_acceso"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('control_acceso.object', {
#             'object': obj
#         })
