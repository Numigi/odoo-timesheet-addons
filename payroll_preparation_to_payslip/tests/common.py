# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Company A'})

        cls.payroll_manager = cls.env['res.users'].create({
            'name': 'payroll@manager.com',
            'login': 'payroll@manager.com',
            'email': 'payroll@manager.com',
            'groups_id': [(4, cls.env.ref('payroll_preparation.group_manager').id)],
            'company_id': cls.company.id,
            'company_ids': [(4, cls.company.id)],
        })
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
        wizard_model = cls.env['payroll.preparation.from.timesheet'].sudo(cls.payroll_manager)
        wizard = wizard_model.create({'period_id': period.id})
        wizard.action_validate()

    @classmethod
    def find_payroll_entries(cls, period):
        return cls.env['payroll.preparation.line'].search([
            ('period_id', '=', period.id),
        ])
