# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo.addons.payroll_preparation.tests.common import PayrollPreparationCase


class TestPayrollPreparationLines(PayrollPreparationCase):

    def test_prorata(self):
        line = self._create_payroll_preperation_line()
        line.amount = 100
        line.prorata = 0.75
        assert line.prorata_amount == 75
