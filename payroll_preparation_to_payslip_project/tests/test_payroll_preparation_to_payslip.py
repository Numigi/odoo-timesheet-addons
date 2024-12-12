# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import PayrollPreparationToPayslipCase


class TestWizard(PayrollPreparationToPayslipCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.entry_1.project_id = cls.project_1.id
        cls.entry_2.project_id = cls.project_1.id

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

    def test_payslip_project(self):
        """Check that the project for payroll entries is
        systematically defined when creating payroll entries"""
        payslip = self._generate_payslips()
        assert payslip.project_id == self.entry_1.project_id

    def test_payslip_project_constraint(self):
        """Check that the payslip creation action cannot be launched on the
        selected payroll entries containing more than one project"""
        self.entry_2.project_id = self.project_2.id
        self._generate_payslips()
        with pytest.raises(ValidationError):
            self._generate_payslips()
