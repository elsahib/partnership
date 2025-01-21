# File: delivery_system/models/delivery_models.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# 1. Delivery Partners
class DeliveryPartner(models.Model):
    _name = "delivery.partner"
    _description = "Delivery Partner"

    name = fields.Char(string="Name", required=True)
    contact_info = fields.Char(string="Contact Information", required=True)
    status = fields.Selection(
        [("active", "Active"), ("pending", "Pending Approval")],
        string="Status",
        default="pending",
    )
    working_blocks = fields.Many2many(
        "delivery.block", string="Assigned Working Blocks"
    )
    completed_deliveries = fields.Integer(string="Completed Deliveries", default=0)
    assigned_routes = fields.One2many(
        "delivery.route", "delivery_partner_id", string="Assigned Routes"
    )
    handled_parcels = fields.One2many(
        "delivery.parcel", "delivery_partner_id", string="Handled Parcels"
    )


# 2. Working Blocks
class DeliveryBlock(models.Model):
    _name = "delivery.block"
    _description = "Working Block"

    date = fields.Date(string="Date", required=True)
    time = fields.Float(string="Time", required=True)
    location = fields.Char(string="Location", required=True)
    number_of_seats = fields.Integer(string="Number of Seats", required=True)
    assigned_partners = fields.Many2many(
        "delivery.partner", string="Assigned Delivery Partners"
    )


# 3. Routes
class DeliveryRoute(models.Model):
    _name = "delivery.route"
    _description = "Delivery Route"

    route_id = fields.Char(string="Route ID", required=True)
    generated_time = fields.Datetime(string="Generated Time", required=True)
    stops = fields.One2many("delivery.stop", "route_id", string="Stops")
    associated_parcels = fields.One2many(
        "delivery.parcel", "route_id", string="Associated Parcels"
    )
    duration = fields.Float(string="Duration (Hours)")
    delivery_partner_id = fields.Many2one(
        "delivery.partner", string="Assigned Delivery Partner", required=True
    )


# 4. Stops
class DeliveryStop(models.Model):
    _name = "delivery.stop"
    _description = "Delivery Stop"

    address = fields.Char(string="Address", required=True)
    stop_type = fields.Selection(
        [("pickup", "Pickup"), ("drop-off", "Drop-off")],
        string="Type",
        required=True,
    )
    associated_parcels = fields.One2many(
        "delivery.parcel", "stop_id", string="Associated Parcels"
    )
    route_id = fields.Many2one("delivery.route", string="Associated Route")


# 5. Parcels
class DeliveryParcel(models.Model):
    _name = "delivery.parcel"
    _description = "Delivery Parcel"

    name = fields.Char(string="Parcel Reference", required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    tracking_id = fields.Char(string="Tracking ID", required=True)
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("pending", "Pending"), ("in_transit", "In Transit"), ("delivered", "Delivered")],
        string="Status",
        default="pending",
    )
    recipient_id = fields.Many2one("res.partner", string="Recipient Details", required=True)
    stop_id = fields.Many2one("delivery.stop", string="Associated Stop")
    route_id = fields.Many2one("delivery.route", string="Associated Route")
    delivery_partner_id = fields.Many2one(
        "delivery.partner", string="Handled By Delivery Partner"
    )


# 6. Pickups
class DeliveryPickup(models.Model):
    _name = "delivery.pickup"
    _description = "Delivery Pickup"

    location = fields.Char(string="Pickup Location", required=True)
    number_of_parcels = fields.Integer(string="Number of Parcels", required=True)
    stop_id = fields.Many2one("delivery.stop", string="Associated Stop")
    central_station_id = fields.Many2one(
        "stock.warehouse", string="Central Station", required=True
    )


# 7. Extend Existing Models
# a. Extend Products
class ProductProduct(models.Model):
    _inherit = "product.product"

    delivery_dimensions = fields.Char(string="Delivery Dimensions")
    delivery_weight = fields.Float(string="Delivery Weight")
    delivery_category = fields.Char(string="Delivery Category")


# b. Extend Orders
class SaleOrder(models.Model):
    _inherit = "sale.order"

    tracking_status = fields.Selection(
        [
            ("created", "Created"),
            ("processing", "Processing"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
        ],
        string="Tracking Status",
        default="created",
    )
    parcel_ids = fields.One2many(
        "delivery.parcel", "sale_order_id", string="Associated Parcels"
    )


# c. Extend Contacts
class ResPartner(models.Model):
    _inherit = "res.partner"

    is_recipient = fields.Boolean(string="Is a Recipient", default=False)
    recipient_details = fields.Text(string="Recipient Details")
