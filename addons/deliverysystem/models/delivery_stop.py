from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeliveryStop(models.Model):
    _name = "delivery.stop"
    _description = "Delivery Stop"

    address = fields.Char(string="Address", required=True)
    stop_type = fields.Selection(
        [("pickup", "Pickup"), ("drop-off", "Drop-off")],
        string="Type",
        required=True,
        default="drop-off",
    )
    status = fields.Selection(
        [("open", "Open"), 
        ("ready_route", "Awaiting Route Assignment"), 
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("not_delivered", "Not Delivered")],
        string="Status",
        default="open",
    )
    associated_parcels = fields.One2many(
        "delivery.parcel", "stop_id", string="Associated Parcels"
    )
    route_id = fields.Many2one("delivery.route", string="Associated Route")
