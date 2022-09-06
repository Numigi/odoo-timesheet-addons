# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollPreparationToPayslip(models.TransientModel):
    _inherit = "payroll.preparation.to.payslip"

    def _get_payslip_vals(self, entries):
        res = super(PayrollPreparationToPayslip, self
                    )._get_payslip_vals(entries)
        res.update({
            "analytic_account_id": entries[0].analytic_account_id.id
        })
        return res
