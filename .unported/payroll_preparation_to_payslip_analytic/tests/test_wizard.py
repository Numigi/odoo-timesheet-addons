# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import PayrollPreparationToPayslipCase


class TestWizard(PayrollPreparationToPayslipCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.entry_1.analytic_account_id = cls.analytic_1.id
        cls.entry_2.analytic_account_id = cls.analytic_1.id

    def _generate_payslips(self):
        active_ids = [self.entry_1.id, self.entry_2.id]
        wizard_model = (
            self.env["payroll.preparation.to.payslip"]
            .with_context(active_ids=active_ids)
            .sudo(self.payroll_manager)
        )
        defaults = wizard_model.default_get([])
        wizard = wizard_model.create(defaults)
        action = wizard.sudo().action_validate()
        domain = action["domain"]
        return self.env["hr.payslip"].search(domain)

    def test_payslip_account_analytic(self):
        """Check that the analytical account for payroll entries is
        systematically defined when creating payroll entries"""
        payslip = self._generate_payslips()
        assert payslip.analytic_account_id == self.entry_1.analytic_account_id

    def test_payslip_creation_for_payroll_entries(self):
        """Check that the payslip creation action cannot be launched on the
        selected payroll entries containing more than one analytical account"""
        self.entry_2.analytic_account_id = self.analytic_2.id
        self._generate_payslips()
        with pytest.raises(ValidationError):
            self._generate_payslips()
