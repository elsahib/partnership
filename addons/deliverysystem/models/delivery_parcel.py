from odoo import models, fields, api
from odoo.exceptions import ValidationError
class DeliveryParcel(models.Model):
    _name = "delivery.parcel"
    _description = "Delivery Parcel"
    prcl_ref = fields.Char(string="Parcel Reference", required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    tracking_id = fields.Char(string="Tracking ID", required=True)
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("pending_packing", "Pending Packing"), 
        ("awaiting_route", "Awaiting Route Assignment"), 
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("not_delivered", "Not Delivered")],
        string="Status",
        default="pending_packing",
    )
    recipient_id = fields.Many2one("res.partner", string="Recipient Details", required=True)
    stop_id = fields.Many2one("delivery.stop", string="Associated Stop")
    route_id = fields.Many2one("delivery.route", string="Associated Route")
    delivery_partner_id = fields.Many2one(
        "res.partner", string="Handled By Delivery Partner"
    )
    parcel_dimensions = fields.Char(string="Parcel Dimensions")
    parcel_weight = fields.Float(string="Parcel Weight")
    parcel_category = fields.Char(string="Parcel Category")
    current_location = fields.Char(string="Current Location", help="Latitude, Longitude")
