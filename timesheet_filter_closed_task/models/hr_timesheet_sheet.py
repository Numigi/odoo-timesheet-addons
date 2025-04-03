# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Sheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    def _task_domain(self):
        domain = [
            ("project_id", "=", self.add_line_project_id.id),
            ("company_id", "=", self.company_id.id),
            ("id", "not in", self.timesheet_ids.mapped("task_id").ids),
            ("stage_id.allow_timesheet", "=", True),
            ("stage_id.closed", "=", False),
        ]
        return domain

    @api.onchange("add_line_project_id")
    def onchange_add_project_id(self):
        """Load the project to the timesheet sheet"""
        if self.add_line_project_id:
            return {
                "domain": {"add_line_task_id": self._task_domain()},
            }
        else:
            return {
                "domain": {
                    "add_line_task_id": [("id", "=", False)],
                },
            }
