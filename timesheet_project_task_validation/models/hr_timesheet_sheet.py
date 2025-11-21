# Copyright 2025 Numigi (tm)
# and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later
# (http://www.gnu.org/licenses/agpl).

from odoo import api, models, exceptions, _


class HrTimesheetSheet(models.Model):
    """
    Extends hr_timesheet.sheet to enforce consistency between
    project and task in the Summary tab.
    """
    _inherit = "hr_timesheet.sheet"

    @api.onchange("add_line_project_id")
    def onchange_add_project_id(self):
        """
        Clear the task to avoid mismatched project/task when
        the project is changed.
        """
        res = super().onchange_add_project_id()
        self.add_line_task_id = False
        return res

    def button_add_line(self):
        """
        Prevent adding a line from the Summary tab when the task
        is missing. Validation is done before calling add_line().
        """
        for rec in self:
            if rec.state in ["new", "draft"]:
                if (
                    rec.add_line_project_id
                    and not rec.add_line_task_id
                ):
                    raise exceptions.ValidationError(
                        _(
                            'Please fill in the "Task" field '
                            "before adding a line."
                        )
                    )
                rec.add_line()
                rec.reset_add_line()

        return True
