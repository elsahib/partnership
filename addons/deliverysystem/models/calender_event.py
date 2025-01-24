from odoo import models, fields, api

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    pay = fields.Float(string="Driver Pay")
    seats_available = fields.Integer(string="Seats Available")
    registration_ids = fields.Many2one('res.partner', string="Registered Drivers")
    route_ids = fields.Many2many('delivery.route', string="Assigned Routes")