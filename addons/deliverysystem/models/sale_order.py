from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
class SaleOrder(models.Model):
    _inherit = "sale.order"
    _logger = logging.getLogger(__name__)

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

    @api.model
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            try:
                # Ensure contact_address exists or use a fallback
                delivery_address = order.partner_id.contact_address or order.partner_id.street or ''            
                stop_values = {
                    'address': delivery_address,
                    'route_id': False
                }
                stop = self.env['delivery.stop'].create(stop_values)
                
                parcel_values = {
                    'prcl_ref': f"Parcel {order.name}-1",
                    'sale_order_id': order.id,
                    'tracking_id': f"TRK{order.id}01",
                    'recipient_id': order.partner_id.id,
                    'stop_id': stop.id,
                }
                self.env['delivery.parcel'].create(parcel_values)
                
                self._logger.info(f"Parcel and stop created for order {order.name}")
            except Exception as e:
                self._logger.error(f"Error creating parcel/stop for order {order.name}: {str(e)}")
        
        return res