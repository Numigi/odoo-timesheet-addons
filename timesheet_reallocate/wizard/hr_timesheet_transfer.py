# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.resource.models.resource import float_to_time

import logging
_logger = logging.getLogger(__name__)


class HrTimesheetTransfer(models.TransientModel):
    """Wizard that allows to define a custom date to post the WIP transfer move."""

    _name = "hr.timesheet.transfer"
    _description = "Timesheet Transfer"

    reason = fields.Char("Reallocation Reason")
    date_time = fields.Datetime(
        "Date", required=True,
        default=fields.Datetime.now,
    )
    project_id = fields.Many2one("project.project", "Project")
    task_id = fields.Many2one(
        "project.task",
        "Task",
        domain="[('project_id', '=', project_id)]",
    )
    timesheet_ids = fields.Many2many(
        "account.analytic.line",
        string="Timesheets",
        readonly=True,
        default=lambda self: self._context.get("timesheet_ids", False),
    )

    def action_transfer(self):
        """
        Create a new timesheet line and write the old ones to negative.
        Validate the wizard to create new timesheet lines with the same
        unit_amount linked to project_id and task_id
        and write the unit_amount of all lines in timesheet_ids to negative.

        """
        self.ensure_one()
        if any(not timesheet.project_id for timesheet in self.timesheet_ids):
            raise UserError(
                _("You cannot reverse an analytic line that is not a timesheet.")
            )
        for timesheet in self.timesheet_ids:
            if timesheet.task_id != self.task_id:
                timesheet_data = timesheet.copy_data()
                timesheet_data[0]['name'] = _(
                            "Timesheet Reallocation - Task %s - %s" % (
                                timesheet.task_id.display_name or "#", timesheet.name
                            )
                        )
                # Create a new line to reallocate time in a target task
                self.env["account.analytic.line"].create({
                    "name": timesheet_data[0]['name'],
                    "project_id": self.project_id.id,
                    "task_id": self.task_id.id,
                    "date_time": self.date_time,
                    "unit_amount": timesheet_data[0]['unit_amount']
                })

                # Create a new line to to deduce time in a source task
                timesheet_data[0]['unit_amount'] = -timesheet_data[0]['unit_amount']
                timesheet.copy(timesheet_data[0])

        self.task_post_message()
        return {"type": "ir.actions.act_window_close"}

    def task_post_message(self):
        """
        Create a note in the chatter of each task.
        """
        self.ensure_one()
        list_tasks = self.timesheet_ids.mapped('task_id')
        # Note in the target task
        target_task_msg = _(
            "Auto reallocation: %s, Tasks: %s" % (
                float_to_time(sum(self.timesheet_ids.mapped('unit_amount'))),
                ", ".join(task.display_name for task in list_tasks)
            )
        )
        self.task_id.message_post(
            subject="Reallocation",
            subtype="mail.mt_note",
            body=target_task_msg
        )

        # Note for every soucre task
        for task in list_tasks:
            task_timsheets = self.timesheet_ids.filtered(lambda t: t.task_id == task)
            task_msg = _(
                "Auto reallocation: - %s, Rallocation Reason: %s, Target Task: %s" % (
                    float_to_time(sum(task_timsheets.mapped('unit_amount'))),
                    self.reason,
                    self.task_id.display_name
                )
            )
            task.message_post(
                subject="Reallocation",
                subtype="mail.mt_note",
                body=task_msg
            )
