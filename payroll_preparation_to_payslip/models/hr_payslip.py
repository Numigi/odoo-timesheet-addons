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
        for rec in self:
            if rec.state in ['draft', 'cancel'] and rec.payroll_entry_ids:
                rec.with_context(
                    force_delete=True).payroll_entry_ids.write({'payslip_id': False})
        return super().unlink()
