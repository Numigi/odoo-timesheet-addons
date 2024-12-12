# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import PayrollPreparationToPayslipCase


class TestPayslip(PayrollPreparationToPayslipCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.amount_1 = 100
        cls.entry_1.amount = cls.amount_1
        cls.entry_1.code = "AAA"

        cls.payslip = cls.env["hr.payslip"].create(
            {
                "employee_id": cls.employee.id,
                "company_id": cls.company.id,
                "contract_id": cls.contract.id,
                "struct_id": cls.structure.id,
                "date_from": cls.date_start,
                "date_to": cls.date_end,
            }
        )
        cls.payslip.payroll_entry_ids = cls.entry_1 | cls.entry_2
        cls.rule = cls.env.ref("hr_payroll.hr_rule_basic")
        cls.rule.write(
            {
                "amount_select": "code",
                "amount_python_compute": "result = entries.AAA",
            }
        )

    def test_compute_rule(self):
        self.payslip.compute_sheet()
        line = self._get_payslip_line()
        assert line.total == self.amount_1

    def test_condition_pass(self):
        self.rule.condition_select = "python"
        self.rule.condition_python = "result = entries.AAA > 50"
        self.payslip.compute_sheet()
        assert self._get_payslip_line()

    def test_condition_fail(self):
        self.rule.condition_select = "python"
        self.rule.condition_python = "result = entries.AAA > 100"
        assert not self._get_payslip_line()

    def test_delete_entry(self):
        with pytest.raises(ValidationError):
            self.entry_1.unlink()

    def _get_payslip_line(self):
        return self.payslip.line_ids.filtered(lambda l: l.salary_rule_id == self.rule)

    def test_delete_draft_payslip_with_payroll_entry_ids(self):
        self.payslip.unlink()

    def test_delete_canceled_payslip_with_payroll_entry_ids(self):
        self.payslip.action_payslip_cancel()
        self.payslip.unlink()
