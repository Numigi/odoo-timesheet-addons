# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.addons.hr_holidays.tests.common import TestHrHolidaysBase


class TestValidateHolidayDate(TestHrHolidaysBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_account_analytic_line_date(self):
        leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Paid Time Off",
                "allocation_type": "fixed",
                "validation_type": "hr",
                "validity_start": False,
            }
        )
        allocation = (
            self.env["hr.leave.allocation"]
            .sudo(self.user_hruser_id)
            .create(
                {
                    "name": "30 days allocation",
                    "holiday_status_id": leave_type.id,
                    "number_of_days": 30,
                    "employee_id": self.employee_emp_id,
                }
            )
        )
        allocation.action_approve()

        # leave 1 only for 1 day or half
        leave1 = (
            self.env["hr.leave"]
            .sudo(self.user_employee_id)
            .create(
                {
                    "name": "Holiday 1 Day",
                    "employee_id": self.employee_emp_id,
                    "holiday_status_id": leave_type.id,
                    "date_from": fields.Datetime.from_string("2023-12-11 08:00:00"),
                    "date_to": fields.Datetime.from_string("2023-12-11 17:00:00"),
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
        date_start = fields.Datetime.from_string("2019-12-27 08:00:00")
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
        # leave2.sudo(self.user_hrmanager_id).action_validate()

        for timesheet_line in leave2.sudo().timesheet_ids:
            self.assertIn(timesheet_line.date, [date_start.date(), date_end.date()])
