# Copyright 2025 Numigi (tm)
# and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later
# (http://www.gnu.org/licenses/agpl).

# -*- coding: utf-8 -*-

from odoo import api, models, exceptions, _


class AccountAnalyticLine(models.Model):
    """
    Validation ensuring that a task is provided when saving analytic
    lines linked to a project in timesheets.
    """
    _inherit = "account.analytic.line"

    @api.constrains("project_id", "task_id")
    def _check_task_required(self):
        """
        Raise an error when a project is set but no task is provided.
        """
        for line in self:
            if line.project_id and not line.task_id:
                raise exceptions.ValidationError(
                    _('Please fill in the "Task" field before saving.')
                )
