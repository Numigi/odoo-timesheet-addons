# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationExportCase(SavepointCase):

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
            'allow_timesheets': True,
        })

        cls.today = datetime.now().date()
        cls.period_1 = cls.create_period(cls.today, cls.today + timedelta(13))
        cls.period_2 = cls.create_period(cls.today - timedelta(14), cls.today - timedelta(1))

    @classmethod
    def create_period(cls, date_from, date_to, company=None):
        return cls.env['payroll.period'].create({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': cls.company.id if company is None else company.id,
        })

    def create_payroll_entry(self, period):
        return self.env['payroll.preparation.line'].create({
            'period_id': period.id,
            'company_id': period.company_id.id,
            'employee_id': self.employee.id,
        })

    @classmethod
    def open_wizard(cls, period):
        wizard_model = cls.env['payroll.preparation.export'].sudo(cls.payroll_manager)
        return wizard_model.create({'period_id': period.id})

    def find_history_entry(cls, period):
        return cls.env['payroll.preparation.export.history'].search([
            ('period_id', '=', period.id),
        ])
