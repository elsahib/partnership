from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
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
    distance = fields.Float(string="Distance (KM)") 
    polyline = fields.Text(string="Polyline")
    def generate_optimized_route(self):
        """Generate optimized route using Google Maps Directions API"""
        if not self.stops:
            return False
        sorted_stops = self.stops.sorted(lambda s: (s.stop_type != 'pickup', s.id))
        origin = sorted_stops[0].address
        destination = sorted_stops[-1].address
        waypoints = [stop.address for stop in sorted_stops[1:-1]]
        maps_helper = self.env['google.maps.helper']
        route_data = maps_helper.optimize_route(origin, destination, waypoints)
        if 'routes' in route_data and route_data['routes']:
            route = route_data['routes'][0]
            self.write({
                'distance': route.get('distanceMeters', 0) / 1000,  # Convert to KM
                'expected_duration': route.get('duration', '0s'),
                'polyline': route.get('polyline', {}).get('encodedPolyline', '')
            })
        return True
    def track_delivery_partner(self):
        if self.delivery_partner_id and self.delivery_partner_id.current_location:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/delivery/track/{self.id}',
                'target': 'new'
            }
        return False
    def action_view_map(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'open_delivery_route_map_modal',
            'target': 'new',
            'name': 'Route Map',
            'params': {
                'route_id': self.id,
            }
        }

    @api.model
    def create_route_from_stops(self, stop_ids=None):
        if stop_ids is None:
            stop_ids = self.env.context.get('default_stop_ids',[])  # Get from context if not passed
        stops = self.env['delivery.stop'].browse(stop_ids)
        if not stops:
            raise UserError('No stops selected')
        route = self.create({
            'route_id': self.env['ir.sequence'].next_by_code('delivery.route'),
            'generated_time': fields.Datetime.now(),
            'stops': [(6, 0, stop_ids)]
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.route',
            'res_id': route.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }
    @api.model
    def action_create_route(self):
        available_stops = self.env['delivery.stop'].search([
            ('route_id', '=', False),
        ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Stops for New Route',
            'view_mode': 'tree,form',
            'res_model': 'delivery.stop',
            'domain': [('id', 'in', available_stops.ids)],
            'context': {
                'default_route_id': False,
                'selection_mode': True
            },
            'target': 'new'
        }