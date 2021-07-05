# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from datetime import timedelta
from odoo.exceptions import ValidationError
from .common import PayrollPreparationCase


@ddt
class TestPayrollPreparationLines(PayrollPreparationCase):

    @data(0, 1, 12, 13)
    def test_date_with_matching_period(self, delta):
        date = self.today + timedelta(delta)
        self._create_payroll_preperation_line(period=self.period, date=date)

    @data(-1, 14)
    def test_if_date_does_not_match_period__raise_error(self, delta):
        date = self.today + timedelta(delta)
        with pytest.raises(ValidationError):
            self._create_payroll_preperation_line(period=self.period, date=date)

    def test_if_no_date__week_not_computed(self):
        line = self._create_payroll_preperation_line(period=self.period, date=None)
        assert not line.week_number

    @data(
        (0, 1),
        (1, 1),
        (6, 1),
        (7, 2),
        (13, 2),
    )
    @unpack
    def test_week_number(self, delta, week_number):
        date = self.today + timedelta(delta)
        line = self._create_payroll_preperation_line(period=self.period, date=date)
        assert line.week_number == week_number
