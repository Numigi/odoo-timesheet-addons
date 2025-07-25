# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Payslip(models.Model):

    _inherit = "hr.payslip"

    payroll_entry_ids = fields.One2many(
        "payroll.preparation.line",
        "payslip_id",
    )
