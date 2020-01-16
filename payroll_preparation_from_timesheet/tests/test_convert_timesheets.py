# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class TestConvertTimesheets(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Company A'})

        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@test.com',
            'email': 'test@test.com',
        })

        cls.employee = cls.env['hr.employee'].create({
            'name': 'John Doe',
            'user_id': cls.user.id,
            'company_id': cls.company.id,
        })

        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
            'company_id': cls.company.id,
            'allow_timesheets': True,
        })

        cls.today = datetime.now().date()
        cls.period = cls._create_period(cls.today, cls.today + timedelta(13))

    @classmethod
    def _create_period(cls, date_from, date_to, company=None):
        return cls.env['payroll.period'].create({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': cls.company.id if company is None else company.id,
        })

    def test_one_entry_created_per_timesheet(self):
        self._create_timesheet(self.today, 1)
        self._create_timesheet(self.today + timedelta(1), 1)
        self._generate_payroll_entries(self.period)
        entries = self._find_payroll_entries(self.period)
        assert len(entries) == 2

    def test_if_ran_twice__payroll_entries_not_generated_twice(self):
        self._create_timesheet(self.today, 1)
        self._generate_payroll_entries(self.period)
        self._generate_payroll_entries(self.period)
        entries = self._find_payroll_entries(self.period)
        assert len(entries) == 1

    def test_timesheet_from_other_period_excluded(self):
        self._create_timesheet(self.today - timedelta(1), 1)
        self._generate_payroll_entries(self.period)
        entries = self._find_payroll_entries(self.period)
        assert len(entries) == 0

    def test_field_propagation(self):
        expected_duration = 10
        expected_date = self.today + timedelta(7)
        self._create_timesheet(expected_date, expected_duration)
        self._generate_payroll_entries(self.period)
        entry = self._find_payroll_entries(self.period)
        assert entry.employee_id == self.employee
        assert entry.analytic_account_id
        assert entry.analytic_account_id == self.project.analytic_account_id
        assert entry.company_id == self.company
        assert entry.duration == expected_duration
        assert entry.date == expected_date

    def _generate_payroll_entries(self, period):
        wizard = self.env['payroll.preparation.from.timesheet'].create({
            'period_id': period.id,
        })
        wizard.action_validate()

    def _create_timesheet(self, date_, hours):
        return self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'employee_id': self.employee.id,
            'company_id': self.company.id,
            'unit_amount': hours,
            'date': date_,
        })

    def _find_payroll_entries(self, period):
        return self.env['payroll.preparation.line'].search([
            ('period_id', '=', period.id),
        ])
