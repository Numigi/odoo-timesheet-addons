# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class PayrollEntry(models.Model):
    _inherit = "payroll.preparation.line"

    def open_payslip_wizard(self):
        self._check_analytic_account()
        return super(PayrollEntry, self).open_payslip_wizard()

    def _check_analytic_account(self):
        if len(self.mapped('analytic_account_id')) > 1:
            raise ValidationError(_(
                "You can process only Entries for a "
                "single Analytic Account at a time."))

