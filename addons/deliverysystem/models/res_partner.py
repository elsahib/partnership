from odoo import models, fields, api
from odoo.exceptions import ValidationError

# 1. Delivery Partners
class ResPartner(models.Model):
    _inherit = "res.partner"

    is_delivery_partner = fields.Boolean(string="Is Delivery Partner",default=False)
    delivery_method = fields.Selection([
        ('car', 'Car'),
        ('motorbike', 'Motorbike'),
    ], string="Delivery Method", default='car')
    delivery_capacity = fields.Integer(string="Delivery Capacity") 
    contact_info = fields.Char(string="Contact Information", required=True)
    status = fields.Selection(
        [("active", "Active"), ("pending", "Pending Approval")],
        string="Status",
        default="pending",
    )
    completed_deliveries = fields.Integer(string="Completed Deliveries", default=0)
    assigned_routes = fields.One2many(
        "delivery.route", "delivery_partner_id", string="Assigned Routes"
    )
    handled_parcels = fields.One2many(
        "delivery.parcel", "delivery_partner_id", string="Handled Parcels"
    )
