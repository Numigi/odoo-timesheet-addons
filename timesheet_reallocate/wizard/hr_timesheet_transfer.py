# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class HrTimesheetTransfer(models.TransientModel):
    """Wizard that allows to define a custom date to post the WIP transfer move."""

    _name = "hr.timesheet.transfer"
    _description = "Timesheet Transfer"

    reason = fields.Char("Reason for Reimputation")
    date_time = fields.Datetime(
        "Date of Reimputation", required=True,
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

        Validate the wizard to create new timesheet lines with the same unit_amount linked to project_id and task_id
        and write the unit_amount of all lines in timesheet_ids to negative.

        """

        if any(not timesheet.project_id for timesheet in self.timesheet_ids):
            raise UserError(
                _("You cannot reverse an analytic line that is not a timesheet.")
            )

        for timesheet in self.timesheet_ids:
            if timesheet.task_id != self.task_id:
                new_timesheet = timesheet.copy(
                    {
                        "project_id": self.project_id.id,
                        "task_id": self.task_id.id,
                        "date_time": self.date_time,
                        "name": _("Reimput of timesheet - Task ")
                        + str(timesheet.task_id.id or "_")
                        + " - "
                        + timesheet.name,
                    }
                )
                timesheet.unit_amount = -timesheet.unit_amount
                timesheet.name = (
                    _("Reimput of timesheet - Task ")
                    + str(new_timesheet.task_id.id or "_")
                    + " - "
                    + timesheet.name
                )
                self.create_note(timesheet, new_timesheet)
        return {"type": "ir.actions.act_window_close"}

    def create_note(self, timesheet, new_timesheet):
        """
        Create a note in the chatter of the timesheet and the new timesheet
        as history of the reimpuation.
        """
        new_timesheet_note = _(
            "Auto reimput of "
            + self.float_to_time(new_timesheet.unit_amount)
            + "<br/> Original task: TA#"
            + str(timesheet.task_id.id or "_")
        )
        timesheet_note = _(
            "Auto reimput of "
            + self.float_to_time(timesheet.unit_amount)
            + "<br/> Reimput reason :"
            + self.reason
            + "<br/> Target task: TA#"
            + str(new_timesheet.task_id.id or "_")
        )
        new_timesheet.message_post(
            subject="Test note", subtype="mail.mt_note", body=new_timesheet_note
        )
        timesheet.message_post(
            subject="Test note", subtype="mail.mt_note", body=timesheet_note
        )

    def float_to_time(self, float_time):
        """
        Convert float to string HH:MM format
        """
        hh = hours = int(float_time)
        minutes = int((float_time - hours) * 60)

        hours = abs(hours)
        minutes = abs(minutes)

        hr = "0" + str(hours) if hours < 10 else str(hours)
        mn = "0" + str(minutes) if minutes < 10 else str(minutes)
        hr = hr if hh > 0 else "-" + hr
        return hr + ":" + mn
