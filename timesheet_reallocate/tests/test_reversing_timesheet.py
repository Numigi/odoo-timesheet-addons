# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.hr_timesheet.tests.test_timesheet import (
    TestCommonTimesheet,
)
from datetime import datetime


class ReversingTimesheet(TestCommonTimesheet):
    def setUp(self):
        super(ReversingTimesheet, self).setUp()


class TestReversingTimesheet(ReversingTimesheet):

    def test_action_transfer(self):
        # Create a timesheet line with project_id and task_id
        timesheet = self.env["account.analytic.line"].create(
            {
                "project_id": self.project_customer.id,
                "task_id": self.task1.id,
                "date_time": datetime.now(),
                "name": "Test Timesheet",
                "unit_amount": 1.35,
            }
        )

        # Create wizard transcient model data to transfer to task 2
        self.wizard = self.env["hr.timesheet.transfer"].create(
            {
                "project_id": self.project_customer.id,
                "task_id": self.task2.id,
                "reason": "Test Reimputation",
                "timesheet_ids": [(6, 0, [timesheet.id])],
            }
        )

        # Call the action_transfer method
        self.wizard.action_transfer()

        timesheet.refresh()

        # Check if the timesheet line is reversed
        self.assertEqual(timesheet.unit_amount, -1.35)

        # Check if new timesheet line is created
        new_timesheet = self.env["account.analytic.line"].search(
            [("unit_amount", "=", 1.35)]
        )
        self.assertTrue(new_timesheet)

        new_timesheet.refresh()

        # Check if new_timesheet description is correct
        new_name = (
            "Reimput of timesheet - Task "
            + str(timesheet.task_id.id or "_")
            + " - "
            + "Test Timesheet"
        )
        self.assertEqual(new_timesheet.name, new_name)

        # Check if new_timesheet project_id is correct
        self.assertEqual(new_timesheet.project_id, self.project_customer)

        # Check if new_timesheet task_id is correct
        self.assertEqual(new_timesheet.task_id, self.task2)

        # Check if new_timesheet date_time is correct
        # Remove the milliseconds from the datetime.now() to compare
        self.assertEqual(new_timesheet.date_time, datetime.now().replace(microsecond=0))

        # Check if timesheet description is correct
        new_name = (
            "Reimput of timesheet - Task "
            + str(new_timesheet.task_id.id or "_")
            + " - "
            + "Test Timesheet"
        )
        self.assertEqual(
            timesheet.name,
            new_name,
        )

        # Check if timesheet unit_amount is correct
        self.assertEqual(timesheet.unit_amount, -1.35)

        # Check if timesheet_note was created on timesheet in chatter
        # Note that <br/> tag is converted by Odoo to <br> tag
        timesheet_template = (
            "<p>Auto reimput of "
            + self.wizard.float_to_time(timesheet.unit_amount)
            + "<br> Reimput reason :"
            + self.wizard.reason
            + "<br> Target task: TA#"
            + str(new_timesheet.task_id.id or "_")
            + "</p>"
        )
        self.assertEqual(
            timesheet.message_ids[0].body,
            timesheet_template,
        )

        # Check if new_timesheet_note was created on new_timesheet in chatter
        # Note that <br/> tag is converted by Odoo to <br> tag
        new_timesheet_template = (
            "<p>Auto reimput of "
            + self.wizard.float_to_time(new_timesheet.unit_amount)
            + "<br> Original task: TA#"
            + str(timesheet.task_id.id or "_")
            + "</p>"
        )
        self.assertEqual(
            new_timesheet.message_ids[0].body,
            new_timesheet_template,
        )

    def test_float_to_time(self):
        self.wizard = self.env["hr.timesheet.transfer"].create({})
        # Check if float_to_time method converts float to time
        self.assertEqual(self.wizard.float_to_time(1.5), "01:30")
        self.assertEqual(self.wizard.float_to_time(12), "12:00")
        self.assertEqual(self.wizard.float_to_time(-2.5), "-02:30")
