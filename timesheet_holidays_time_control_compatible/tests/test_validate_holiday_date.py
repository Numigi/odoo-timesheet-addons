# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.addons.hr_holidays.tests.common import TestHrHolidaysBase


class TestValidateHolidayDate(TestHrHolidaysBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_account_analytic_line_date(self):
        employee = self.employee_emp
        leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Paid Time Off",
                "request_unit": "hour",
                "leave_validation_type": "both",
            }
        )
        allocation = self.env["hr.leave.allocation"].create(
            {
                "name": "30 days allocation",
                "holiday_status_id": leave_type.id,
                "number_of_days": 30,
                "employee_id": employee.id,
            }
        )
        allocation.action_approve()

        # leave 1 only for 1 day or half
        leave1 = self.env["hr.leave"].create(
            {
                "name": "Holiday 1 Day",
                "employee_id": employee.id,
                "holiday_status_id": leave_type.id,
                "date_from": fields.Datetime.from_string("2019-12-09 08:00:00"),
                "date_to": fields.Datetime.from_string("2019-12-09 17:00:00"),
                "number_of_days": 1,
            }
        )
        leave1.action_approve()
        leave1.action_validate()
        self.assertEqual(
            leave1.timesheet_ids[0].date, leave1.date_from.date(), msg=None)

        # leave 2 more than 1 day
        date_start = fields.Datetime.from_string("2019-12-16 08:00:00")
        date_end = fields.Datetime.from_string("2019-12-17 17:00:00")
        leave2 = self.env["hr.leave"].create(
            {
                "name": "Holiday 3 Days",
                "employee_id": employee.id,
                "holiday_status_id": leave_type.id,
                "date_from": date_start,
                "date_to": date_end,
                "number_of_days": 2,
            }
        )
        leave2.action_approve()
        leave2.action_validate()

        for timesheet_line in leave2.timesheet_ids:
            self.assertIn(
                timesheet_line.date,
                [date_start.date(), date_end.date()])
