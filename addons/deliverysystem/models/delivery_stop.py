from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
class DeliveryStop(models.Model):
    _name = "delivery.stop"
    _description = "Delivery Stop"
    _order = "sequence, id"
    sequence = fields.Integer(string="Sequence", default=10)
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
    def create_route_from_stops(self):
        active_model = self.env.context.get('active_model')
        if not active_model:
            raise UserError(_("Active model not found in context."))

        selected_records = self.env[active_model].browse(self.env.context.get('active_ids', []))

        if not selected_records:
            raise UserError(_("No records selected."))

        stop_ids = selected_records.ids

        route = self.env['delivery.route'].create({
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