# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class PayrollPreparationToPayslip(models.TransientModel):
    _inherit = "payroll.preparation.to.payslip"

    def _get_payslip_vals(self, entries):
        res = super(PayrollPreparationToPayslip, self
                    )._get_payslip_vals(entries)
        res.update({
            "project_id": entries[0].project_id.id
        })
        return res
