# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from odoo.tests import common
from datetime import timedelta, date, datetime


@ddt
class TestAccountAnalyticLine(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.tz = False
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "A1",}
        )

    @data(datetime(2016, 3, 24, 3), "2016-03-24 03:00:00")
    def test_create_analytic_line_with_datetime(self, datetime_):
        line = self._create_analytic_line_with_datetime(datetime_, tz="EST")
        self.assertEqual(line.date, date(2016, 3, 23))

    @data(datetime(2016, 3, 24, 3), "2016-03-24 03:00:00")
    def test_write_analytic_line_with_datetime(self, datetime_):
        line = self._create_analytic_line_with_datetime(datetime.now())
        line.with_context(tz="EST").date_time = datetime_
        self.assertEqual(line.date, date(2016, 3, 23))

    @data(date(2016, 3, 24), "2016-03-24")
    def test_create_analytic_line_with_date(self, date_):
        line = self._create_analytic_line_with_date(date_, tz="EST")
        self.assertEqual(line.date_time, datetime(2016, 3, 24, 5))

    @data(date(2016, 3, 24), "2016-03-24")
    def test_write_analytic_line_with_date(self, date_):
        line = self._create_analytic_line_with_datetime(datetime.now())
        line.with_context(tz="EST").date = date_
        self.assertEqual(line.date_time, datetime(2016, 3, 24, 5))

    def test_if_no_timezone_given__use_user_tz(self):
        date_ = date(2016, 3, 24)
        self.env.user.tz = "EST"
        line = self._create_analytic_line_with_date(date_, tz=False)
        self.assertEqual(line.date_time, datetime(2016, 3, 24, 5))

    def test_if_no_timezone_given__and_user_has_no_tz__use_utc(self):
        date_ = date(2016, 3, 24)
        line = self._create_analytic_line_with_date(date_, tz=False)
        self.assertEqual(line.date_time, datetime(2016, 3, 24, 0))

    def _create_analytic_line_with_datetime(self, datetime_, tz=None):
        return (
            self.env["account.analytic.line"]
            .with_context(tz=tz)
            .create(
                {
                    "name": "Test line",
                    "date_time": datetime_,
                    "account_id": self.analytic_account.id,
                }
            )
        )

    def _create_analytic_line_with_date(self, date_, tz=None):
        return (
            self.env["account.analytic.line"]
            .with_context(tz=tz)
            .create(
                {
                    "name": "Test line",
                    "date": date_,
                    "account_id": self.analytic_account.id,
                }
            )
        )
