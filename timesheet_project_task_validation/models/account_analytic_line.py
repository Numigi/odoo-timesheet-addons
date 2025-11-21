# Copyright 2025 Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


# -*- coding: utf-8 -*-
from odoo import api, models, exceptions, _


class AccountAnalyticLine(models.Model):
    """
    Adds a validation on analytic line entries created from timesheets.
    A task is required when saving any analytic line coming from timesheets.
    """
    _inherit = "account.analytic.line"

    @api.constrains("project_id", "task_id")
    def _check_task_required(self):
        """
        Ensure that a task is provided when a project is set.
        This avoids overriding create/write, preserving native logic
        from hr_timesheet_sheet.
        """
        for line in self:
            if line.project_id and not line.task_id:
                raise exceptions.ValidationError(
                    _('Please fill in the "Task" field before saving.')
                )