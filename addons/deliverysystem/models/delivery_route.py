from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeliveryRoute(models.Model):
    _name = "delivery.route"
    _description = "Delivery Route"

    route_id = fields.Char(string="Route ID", required=True)
    generated_time = fields.Datetime(string="Generated Time", required=True, default=fields.Datetime.now)
    stops = fields.One2many("delivery.stop", "route_id", string="Stops")
    delivery_partner_id = fields.Many2one(
        "hr.employee", string="Assigned Delivery Partner"
    )
    expected_duration = fields.Float(string="Expected Duration (Hours)")
    event_id = fields.Many2one('block.schedule', string="Delivery Block")
    google_maps_route_id = fields.Char(string="Google Maps Route ID") 
    estimated_arrival_time = fields.Datetime(string="Estimated Arrival Time")
    distance = fields.Float(string="Distance (KM)") 
    polyline = fields.Text(string="Polyline")
  