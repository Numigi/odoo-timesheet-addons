# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Payslip(models.Model):

    _inherit = "hr.payslip"

    payroll_entry_ids = fields.One2many(
        "payroll.preparation.line",
        "payslip_id",
    )

    def unlink(self):
        if self.state in ['draft', 'cancel'] and self.payroll_entry_ids:
            self.with_context(
                force_delete=True).payroll_entry_ids.payslip_id = False
            return super().unlink()
        else:
            return super().unlink()
