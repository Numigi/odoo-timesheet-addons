# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Company A'})

        cls.today = datetime.now().date()
        cls.period = cls._create_period(cls.today, cls.today + timedelta(13))
        cls.employee = cls.env['hr.employee'].create({
            'name': 'John Doe',
        })

    @classmethod
    def _create_period(cls, date_from, date_to, company=None):
        return cls.env['payroll.period'].create({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': cls.company.id if company is None else company.id,
        })

    @classmethod
    def _create_payroll_preperation_line(cls, period=None, date=None, company=None):
        return cls.env['payroll.preparation.line'].create({
            'period_id': (period or cls.period).id,
            'date': date if date else None,
            'company_id': (company or cls.company).id,
            'employee_id': cls.employee.id,
        })
