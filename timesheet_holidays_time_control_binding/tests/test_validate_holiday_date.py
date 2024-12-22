# Copyright 2023-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.addons.hr_holidays.tests.common import TestHrHolidaysCommon


class TestValidateHolidayDate(TestHrHolidaysCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_account_analytic_line_date(self):
        leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Paid Time Off",
                "leave_validation_type": "hr",
            }
        )
        allocation = (
            self.env["hr.leave.allocation"]
            .with_user(self.user_hruser_id)
            .create(
                {
                    "name": "30 days allocation",
                    "holiday_status_id": self.env.ref(
                        "hr_holidays.holiday_status_training"
                    ).id,
                    "number_of_days": 30,
                    "employee_id": self.employee_emp_id,
                }
            )
        )
        allocation.action_validate()

        # leave 1 only for 1 day or half
        leave1 = (
            self.env["hr.leave"]
            .with_user(self.user_employee_id)
            .create(
                {
                    "name": "Holiday 1 Day",
                    "employee_id": self.employee_emp_id,
                    "holiday_status_id": leave_type.id,
                    "date_from": fields.Datetime.from_string("2023-09-20 08:00:00"),
                    "date_to": fields.Datetime.from_string("2023-09-20 17:00:00"),
                    "number_of_days": 1,
                }
            )
        )
        leave1.sudo().action_approve()

        self.assertEqual(
            leave1.sudo().timesheet_ids[0].date,
            leave1.sudo().date_from.date(),
            msg=None,
        )

        # leave 2 more than 1 day
        date_start = fields.Datetime.from_string("2019-12-26 08:00:00")
        date_end = fields.Datetime.from_string("2019-12-29 17:00:00")
        leave2 = self.env["hr.leave"].create(
            {
                "name": "Holiday 3 Days",
                "employee_id": self.employee_emp_id,
                "holiday_status_id": leave_type.id,
                "request_date_from": date_start,
                "request_date_to": date_end,
                "number_of_days": 2,
            }
        )
        leave2.sudo().action_approve()

        for timesheet_line in leave2.sudo().timesheet_ids:
            self.assertIn(timesheet_line.date_time, [date_start, date_end])
