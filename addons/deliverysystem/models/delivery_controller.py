from odoo import models, api
from googlemaps import Client as GoogleMapsClient
class DeliveryController(models.Model):
    _name = 'delivery.controller'
    @api.model
    def create_route(self, stop_ids):
        stops = self.env['delivery.stop'].browse(stop_ids)
        # Use Google Maps API to optimize the route
        gmaps = GoogleMapsClient(key=self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key'))
        route_info = gmaps.directions(
            [stop.address for stop in stops],
            optimize_waypoints=True
        )
        route = self.env['delivery.route'].create({
            'stops': [(0, 0, {'address': stop.address, 'stop_type': stop.type, 'status': stop.status}) for stop in stops],
            'polyline': route_info['overview_polyline']['points'],
            'distance': route_info['legs'][0]['distance']['value'],
            'expected_duration': sum(leg['duration']['value'] for leg in route_info['legs']),
        })
        return {'route_id': route.id}