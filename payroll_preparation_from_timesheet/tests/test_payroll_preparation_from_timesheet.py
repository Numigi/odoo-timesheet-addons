# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from .common import PayrollPreparationCase


class TestPayrollPreparationFromTimesheet(PayrollPreparationCase):

    def test_one_entry_created_per_timesheet(self):
        self.create_timesheet(self.today, 1)
        self.create_timesheet(self.today + timedelta(1), 1)
        self.generate_payroll_entries(self.period)
        entries = self.find_payroll_entries(self.period)
        assert len(entries) == 2

    def test_if_ran_twice__payroll_entries_not_generated_twice(self):
        self.create_timesheet(self.today, 1)
        self.generate_payroll_entries(self.period)
        self.generate_payroll_entries(self.period)
        entries = self.find_payroll_entries(self.period)
        assert len(entries) == 1

    def test_timesheet_from_other_period_excluded(self):
        self.create_timesheet(self.today - timedelta(1), 1)
        self.generate_payroll_entries(self.period)
        entries = self.find_payroll_entries(self.period)
        assert len(entries) == 0

    def test_field_propagation(self):
        expected_duration = 10
        expected_date = self.today + timedelta(7)
        self.create_timesheet(expected_date, expected_duration)
        self.generate_payroll_entries(self.period)
        entry = self.find_payroll_entries(self.period)
        assert entry.employee_id == self.employee
        assert entry.analytic_account_id
        assert entry.analytic_account_id == self.project.analytic_account_id
        assert entry.company_id == self.company
        assert entry.duration == expected_duration
        assert entry.date == expected_date
