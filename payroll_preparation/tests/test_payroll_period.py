# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


@ddt
class TestPayrollPeriods(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Company A'})
        cls.other_company = cls.env['res.company'].create({'name': 'Company B'})

        cls.today = datetime.now().date()
        cls.period_today = cls._create_period(cls.today, cls.today + timedelta(6))

    @classmethod
    def _create_period(cls, date_from, date_to, company=None):
        return cls.env['payroll.preparation.line'].create({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': cls.company.id if company is None else company.id,
        })

    @data(
        (6, 13),
        (-6, 0),
    )
    @unpack
    def test_if_overlaping_date_range__error_raised(self, date_from_delta, date_to_delta):
        with pytest.raises(ValidationError):
            self._create_period(
                self.today + timedelta(date_from_delta),
                self.today + timedelta(date_to_delta),
            )

    def test_if_different_company_overlaping_period__error_raised(self):
        assert self.period_today.copy({'company_id': self.other_company.id})

    @classmethod
    def _find_period(cls, date_, company=None):
        return cls.env['payroll.preparation.line'].find_period(date_, company or cls.company)

    @data(0, 1, 5, 6)
    def test_find_period(self, delta):
        result = self._find_period(self.today + timedelta(delta))
        assert result == self.period_today

    @data(-1, 7)
    def test_find_period__case_with_no_period_defined(self, delta):
        result = self._find_period(self.today + timedelta(delta))
        assert not result

    def test_find_period__case_no_period_for_given_company(self):
        result = self._find_period(self.today + timedelta(1), self.other_company)
        assert not result
