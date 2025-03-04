import requests
from odoo import models
from odoo.exceptions import UserError
import googlemaps

class GoogleMapsHelper(models.AbstractModel):
    _name = 'google.maps.helper'
    _description = 'Google Maps Integration Helper'

    def get_api_key(self):
        return self._get_api_key()
        
    def get_map_id(self):
        return self.env['ir.config_parameter'].sudo().get_param('deliverysystem.google_maps_map_id')

    def _get_api_key(self):
        return self.env['ir.config_parameter'].sudo().get_param('deliverysystem.google_maps_api_key')

    def optimize_route(self, origin, destination, waypoints):
        api_key = self._get_api_key()
        if not api_key:
            raise UserError('Google Maps API key not configured')
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        waypoint_locations = [{"address": wp} for wp in waypoints]
        payload = {
            "origin": {"address": origin},
            "destination": {"address": destination},
            "intermediates": waypoint_locations,
            "travelMode": "DRIVE",
            "polylineQuality":"HIGH_QUALITY",
            "routingPreference": "TRAFFIC_AWARE",
            "computeAlternativeRoutes": False,
            "languageCode": "en-US",
            "units": "METRIC"
        }
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.legs"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def reverse_geocode(self, latitude, longitude):
        """Reverse geocode a latlng to an address using Google Maps API."""
        api_key = self.env['ir.config_parameter'].sudo().get_param('deliverysystem.google_maps_api_key')
        if not api_key:
            raise UserError("Google Maps API key is not configured. Please configure it in Delivery System settings.")
        
        gmaps = googlemaps.Client(key=api_key)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
            return reverse_geocode_result
        except Exception as e:
            return False

    def geocode(self, address):
        api_key = self.env['ir.config_parameter'].sudo().get_param('deliverysystem.google_maps_api_key')
        if not api_key:
            raise UserError("Google Maps API key is not configured. Please configure it in Delivery System settings.")
        
        gmaps = googlemaps.Client(key=api_key)
        try:
            geocode_result = gmaps.geocode(address)
            
            return geocode_result
        except Exception as e:
            return False

    def update_location(self, lat, lng):
        """Update current location for delivery partner"""
        if not self.env.user.partner_id.is_delivery_partner:
            return False
        self.env.user.partner_id.write({
            'current_location': f"{lat},{lng}"
        })
        return True