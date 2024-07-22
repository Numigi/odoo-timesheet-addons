# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.hr_timesheet.tests.test_timesheet import (
    TestCommonTimesheet,
)
from odoo.addons.resource.models.resource import float_to_time

from datetime import datetime


class TestReversingTimesheet(TestCommonTimesheet):

    def setUp(self):
        super(TestReversingTimesheet, self).setUp()

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
        self.assertEquals(len(self.task1.timesheet_ids), 2,
                          "Reverset timesheet should be added to task 1")
        self.assertEqual(self.task1.timesheet_ids[1].unit_amount, -1.35,
                         "Reverset timesheet sould be equal to -1.35")
        self.assertEquals(len(self.task2.timesheet_ids), 1,
                          "New timesheet should be added to task 2")
        self.assertEqual(self.task2.timesheet_ids[0].unit_amount, 1.35,
                         "Reverset timesheet sould be equal to 1.35")

        # Check if new_timesheet description is correct
        new_name = "Timesheet Reallocation - Task %s - %s" % (
            timesheet.task_id.display_name, timesheet.name
        )
        self.assertEqual(self.task2.timesheet_ids[0].name, new_name)

        # Check if new_timesheet project_id is correct
        self.assertEqual(self.task2.timesheet_ids[0].project_id,
                         self.project_customer)

        # Check if new_timesheet task_id is correct
        self.assertEqual(self.task2.timesheet_ids[0].task_id, self.task2)

        # Check if new_timesheet date_time is correct
        self.assertEqual(self.task2.timesheet_ids[0].date_time,
                         datetime.now().replace(microsecond=0))

        # Check the note added in the source task in chatter
        task_msg = (
                "<p>Auto reallocation: - %s, Rallocation Reason: %s, Target Task: %s</p>" % (
                    float_to_time(self.task1.timesheet_ids[0].unit_amount),
                    "Test Reimputation",
                    self.task2.display_name
                )
            )
        self.assertEqual(
            self.task1.message_ids[0].body,
            task_msg,
        )

        # Check the note added in the target task in chatter
        task_msg = (
                "<p>Auto reallocation: %s, Tasks: %s</p>" % (
                    float_to_time(self.task2.timesheet_ids[0].unit_amount),
                    self.task1.display_name
                )
            )
        self.assertEqual(
            self.task2.message_ids[0].body,
            task_msg,
        )
