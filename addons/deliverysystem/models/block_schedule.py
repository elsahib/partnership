from odoo import models, fields, api
from odoo.exceptions import ValidationError
class BlockSchedule(models.Model):
    _name = "block.schedule"
    _description = "Delivery Block Schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string="Block Name", required=True, tracking=True)
    start_datetime = fields.Datetime(string="Start Time", required=True, tracking=True)
    end_datetime = fields.Datetime(string="End Time", required=True, tracking=True)
    pay = fields.Float(string="Driver Pay", tracking=True)
    seats_available = fields.Integer(string="Total Seats", default=1, tracking=True)
    remaining_seats = fields.Integer(string="Remaining Seats", compute='_compute_remaining_seats', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open for Registration'),
        ('full', 'Fully Booked'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)
    driver_ids = fields.Many2many(
        'res.partner', 
        string="Registered Drivers",
        domain=[('is_delivery_partner', '=', True)],
        tracking=True
    )
    route_ids = fields.Many2many('delivery.route', string="Assigned Routes", tracking=True)
    company_id = fields.Many2one('res.company', string='Company', 
                                default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='Responsible', 
                             default=lambda self: self.env.user,
                             tracking=True)
    notes = fields.Text(string="Notes")
    @api.depends('seats_available', 'driver_ids')
    def _compute_remaining_seats(self):
        for block in self:
            registered_drivers = len(block.driver_ids)
            block.remaining_seats = block.seats_available - registered_drivers
            # Auto-update state if fully booked
            if block.remaining_seats == 0 and block.state == 'open':
                block.state = 'full'
            elif block.remaining_seats > 0 and block.state == 'full':
                block.state = 'open'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_dates(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.start_datetime >= record.end_datetime:
                    raise ValidationError("End time must be after start time")

    @api.constrains('driver_ids')
    def _check_seats_limit(self):
        for record in self:
            if len(record.driver_ids) > record.seats_available:
                raise ValidationError(
                    f"Cannot exceed the number of available seats ({record.seats_available})"
                )

    def action_open_registration(self):
        self.ensure_one()
        self.write({'state': 'open'})
        return True

    def action_register(self):
        self.ensure_one()
        if self.state != 'open':
            raise ValidationError("This block is not open for registration")
        if self.remaining_seats <= 0:
            raise ValidationError("No seats available for this block")
        current_user_partner = self.env.user.partner_id
        if not current_user_partner.is_delivery_partner:
            raise ValidationError("Only delivery partners can register for blocks")
        if current_user_partner in self.driver_ids:
            raise ValidationError("You are already registered for this block")
        if conflicting_blocks := self.search(
            [
                ('id', '!=', self.id),
                ('driver_ids', 'in', [current_user_partner.id]),
                ('start_datetime', '<', self.end_datetime),
                ('end_datetime', '>', self.start_datetime),
                ('state', 'in', ['open', 'full', 'in_progress']),
            ]
        ):
            raise ValidationError(
                "You have a schedule conflict with another block during this time period"
            )

        self.write({
            'driver_ids': [(4, current_user_partner.id)]
        })
        return True
    def action_unregister(self):
        """Action for a driver to unregister from this block"""
        self.ensure_one()
        if self.state not in ['open', 'full']:
            raise ValidationError("Cannot unregister from this block at its current state")
        current_user_partner = self.env.user.partner_id
        if current_user_partner not in self.driver_ids:
            raise ValidationError("You are not registered for this block")
        self.write({
            'driver_ids': [(3, current_user_partner.id)]
        })
        return True

    def action_start(self):
        self.write({'state': 'in_progress'})
        return True

    def action_complete(self):
        self.write({'state': 'completed'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_draft(self):
        self.write({
            'state': 'draft',
            'driver_ids': [(5, 0, 0)]  # Clear all registered drivers
        })
        return True