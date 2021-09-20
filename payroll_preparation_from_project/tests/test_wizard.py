# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import timedelta
from odoo.exceptions import AccessError
from .common import PayrollPreparationCase


class TestWizard(PayrollPreparationCase):
    def test_open_wizard(self):
        action = self.project.open_payroll_preparation_wizard()
        assert action["res_model"] == "payroll.preparation.from.project"
        assert action["context"]["default_project_id"] == self.project.id

    def test_wizard_validate(self):
        wizard = self.env["payroll.preparation.from.project"].create(
            {
                "project_id": self.project.id,
            }
        )
        action = wizard.action_validate()
        assert action["res_model"] == "payroll.preparation.line"
        assert action["context"]["search_default_project_id"] == self.project.id
