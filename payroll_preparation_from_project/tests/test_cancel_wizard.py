# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import timedelta
from odoo.exceptions import AccessError
from .common import PayrollPreparationCase


class TestWizard(PayrollPreparationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.line = cls.env["payroll.preparation.line"].create(
            {
                "employee_id": cls.employee.id,
                "company_id": cls.company.id,
                "project_id": cls.project.id,
            }
        )

    def test_wizard_validate(self):
        assert self.project.payroll_entry_count == 1
        self._run_wizard()
        assert self.project.payroll_entry_count == 0
        assert not self.line.exists()

    def _run_wizard(self):
        wizard = self.env["payroll.preparation.project.cancel"].create(
            {
                "project_ids": [(4, self.project.id)],
            }
        )
        wizard.action_validate()
