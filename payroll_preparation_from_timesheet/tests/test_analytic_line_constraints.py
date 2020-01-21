# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import PayrollPreparationCase


class TestAnalyticLineConstraints(PayrollPreparationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = cls.env.ref('base.user_admin')
        cls.admin_user.company_ids |= cls.company
        cls.admin_user.company_id = cls.company
        cls.super_user = cls.env.ref('base.user_root')

    def test_if_has_payroll_entry__analytic_line_can_not_be_deleted(self):
        line = self.create_timesheet(self.today, 1)
        self.generate_payroll_entries(self.period)
        with pytest.raises(ValidationError):
            line.unlink()

    def test_if_has_payroll_entry__analytic_line_can_not_be_modified(self):
        line = self.create_timesheet(self.today, 1)
        self.generate_payroll_entries(self.period)
        with pytest.raises(ValidationError):
            line.sudo(self.admin_user).unit_amount = 10

    def test_if_is_super_admin__analytic_line_can_be_modified(self):
        line = self.create_timesheet(self.today, 1)
        self.generate_payroll_entries(self.period)
        new_value = 10
        line.sudo(self.super_user).unit_amount = new_value
        assert line.unit_amount == new_value

    def test_if_has_no_payroll_entry__analytic_line_can_be_modified(self):
        line = self.create_timesheet(self.today, 1)
        new_value = 10
        line.sudo(self.admin_user).unit_amount = new_value
        assert line.unit_amount == new_value
