# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


@ddt
class TestPeriodConstraints(SavepointCase):

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

    @data(0, 1, 12, 13)
    def test_date_with_matching_period(self, delta):
        date = self.today + timedelta(delta)
        self._create_payroll_preperation_line(period=self.period, date=date)

    @data(-1, 14)
    def test_if_date_does_not_match_period__raise_error(self, delta):
        date = self.today + timedelta(delta)
        with pytest.raises(ValidationError):
            self._create_payroll_preperation_line(period=self.period, date=date)

    def _create_payroll_preperation_line(self, period, date):
        return self.env['payroll.preparation.line'].create({
            'period_id': period.id,
            'date': date,
            'company_id': period.company_id.id,
            'employee_id': self.employee.id,
        })

    @data(
        (0, 1),
        (1, 1),
        (6, 1),
        (7, 2),
        (13, 2),
    )
    @unpack
    def test_week(self, delta, week):
        date = self.today + timedelta(delta)
        line = self._create_payroll_preperation_line(period=self.period, date=date)
        assert line.week == week
