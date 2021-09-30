# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from .common import PayrollPreparationToPayslipCase


class TestWizard(PayrollPreparationToPayslipCase):

    def _generate_payslips(self):
        active_ids = [self.entry_1.id, self.entry_2.id]
        wizard_model = (
            self.env["payroll.preparation.to.payslip"]
            .with_context(active_ids=active_ids)
            .sudo(self.payroll_manager)
        )
        defaults = wizard_model.default_get([])
        wizard = wizard_model.create(defaults)
        action = wizard.action_validate()
        domain = action["domain"]
        return self.env["hr.payslip"].search(domain)

    def test_single_payslip(self):
        payslip = self._generate_payslips()
        assert len(payslip) == 1

    def test_two_different_employees(self):
        employee_2 = self.employee.copy()
        self.entry_2.employee_id = employee_2
        payslip = self._generate_payslips()
        assert len(payslip) == 2

    def test_employee_contract_selected(self):
        payslip = self._generate_payslips()
        assert payslip.contract_id == self.contract
        assert payslip.struct_id == self.structure

    def test_entry_without_date(self):
        self.entry_1.date = False
        with pytest.raises(ValidationError):
            self._generate_payslips()

    def test_generate_payslip_twice(self):
        self._generate_payslips()
        with pytest.raises(ValidationError):
            self._generate_payslips()
