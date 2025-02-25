# addons/deliverysystem/models/delivery_dashboard.py
from odoo import models, fields, api

class DeliveryDashboard(models.Model):
    _name = 'delivery.dashboard'
    _description = 'Delivery System Dashboard'

    name = fields.Char(default='Dashboard')
    total_parcels = fields.Integer(compute='_compute_dashboard_data')
    parcels_delivered = fields.Integer(compute='_compute_dashboard_data')
    active_routes = fields.Integer(compute='_compute_dashboard_data')
    active_drivers = fields.Integer(compute='_compute_dashboard_data')

    def init(self):
        """Create a default dashboard record if none exists"""
        if not self.search([]):
            self.create({'name': 'Main Dashboard'})

    @api.depends('name')
    def _compute_dashboard_data(self):
        for record in self:
            # Total parcels
            record.total_parcels = self.env['delivery.parcel'].search_count([])
            
            # Parcels delivered today
            record.parcels_delivered = self.env['delivery.parcel'].search_count([
                ('status', '=', 'delivered'),
                ('create_date', '>=', fields.Date.today())
            ])
            
            # Active routes
            record.active_routes = self.env['delivery.route'].search_count([
                ('delivery_partner_id', '!=', False)
            ])
            
            # Active drivers
            record.active_drivers = self.env['res.partner'].search_count([
                ('is_delivery_partner', '=', True),
                ('status', '=', 'active')
            ])