# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class PayrollPreparationToPayslip(models.TransientModel):

    _name = 'payroll.preparation.to.payslip'
    _description = 'Payroll Preparation To Payslip'

    entry_ids = fields.Many2one("payroll.preparation.line")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_ids = self._context.get("active_ids") or []
        res["entry_ids"] = [(6, 0, active_ids)]

        return res

    def action_validate(self):
        self._generate_payslips()
        return self._get_payslip_list_action()

    def _generate_payslips(self):
        pass

    def _get_payslip_list_action(self):
        pass
