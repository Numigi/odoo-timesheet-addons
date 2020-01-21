# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationCase(SavepointCase):

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
        cls.period = cls.create_period(cls.today, cls.today + timedelta(13))

    @classmethod
    def create_period(cls, date_from, date_to, company=None):
        return cls.env['payroll.period'].create({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': cls.company.id if company is None else company.id,
        })

    @classmethod
    def generate_payroll_entries(cls, period):
        wizard = cls.env['payroll.preparation.from.timesheet'].create({
            'period_id': period.id,
        })
        wizard.action_validate()

    @classmethod
    def create_timesheet(cls, date_, hours):
        return cls.env['account.analytic.line'].create({
            'name': '/',
            'project_id': cls.project.id,
            'employee_id': cls.employee.id,
            'company_id': cls.company.id,
            'unit_amount': hours,
            'date': date_,
        })

    @classmethod
    def find_payroll_entries(cls, period):
        return cls.env['payroll.preparation.line'].search([
            ('period_id', '=', period.id),
        ])
