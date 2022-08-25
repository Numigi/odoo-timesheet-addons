# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollEntry(models.Model):

    _inherit = "payroll.preparation.line"

    payslip_id = fields.Many2one(
        "hr.payslip", index=True, ondelete="restrict", copy=False,
    )

    def open_payslip_wizard(self):
        action = self.env.ref(
            "payroll_preparation_to_payslip.payslip_wizard_action"
        ).read()[0]
        action["context"] = {"active_ids": self._context.get("active_ids")}
        return action

    def write(self, vals):
        payslips = self.mapped("payslip_id")

        if payslips:
            raise ValidationError(
                _(
                    "You cannot modify a Payroll Entry once a Payslip "
                    "is linked to the Payroll Entry"
                ).format(
                    ", ".join(payslips.mapped("display_name"))
                )
            )

        return super().write(vals)

    def unlink(self):
        payslips = self.mapped("payslip_id")

        if payslips:
            raise ValidationError(
                _(
                    "The payroll entries are already included in payslips ({}). "
                    "\n\n"
                    "To apply corrections, please manually create a new payslip "
                    "or new payroll entries."
                ).format(
                    ", ".join(payslips.mapped("display_name"))
                )
            )

        return super().unlink()
