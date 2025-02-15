from odoo import fields, models
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    google_maps_api_key = fields.Char(
        string='Google Maps API Key',
        config_parameter='deliverysystem.google_maps_api_key',
        help="API key for Google Maps integration"
    )
    google_maps_map_id = fields.Char(
        string='Google Maps Map ID',
        config_parameter='deliverysystem.google_maps_map_id',
        help='Google Maps Map ID for web map'
    )