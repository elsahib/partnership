# File: delivery_system/models/res_users.py
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    ROLE_SELECTION = [
        ("admin", "Admin"),
        ("driver", "Driver"),
        ("customer", "Customer"),
        ("warehouse", "Warehouse"),
    ]

    role = fields.Selection(
        ROLE_SELECTION,
        string="Role",
        default="customer",  # Default role for new users
        required=True,
    )
