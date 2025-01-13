# -*- coding: utf-8 -*-

# from odoo import models, fields, api

# class IrHttp(models.AbstractModel):
#     _inherit = "ir.http"

#     @classmethod
#     def _auth_method_my_api_key(cls):
#         api_key = request.httprequest.headers.get("Authorization")
#         if not api_key:
#             raise BadRequest("Authorization header with API key missing")

#         user_id = request.env["res.users.apikeys"]._check_credentials(
#             scope="rpc", key=api_key
#         )
#         if not user_id:
#             raise BadRequest("API key invalid")

#         request.uid = user_id 


# class odoocontroller(models.Model):
#     _name = 'odoocontroller.odoocontroller'
#     _description = 'odoocontroller.odoocontroller'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



