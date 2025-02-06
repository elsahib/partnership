from odoo import models, fields
class HrEmployee(models.Model):
    _inherit = "hr.employee"
    delivery_schedule = fields.Text(string="Delivery Schedule") # Example: Simple text or a link to an external schedule 
    current_location = fields.Char(string="Current Location", help="Latitude, Longitude")
