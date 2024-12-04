# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _task_domain(self):
        domain = [
            ("project_id", "=", self.project_id.id),
            ("stage_id.allow_timesheet", "=", True),
            ("stage_id.closed", "=", False),
        ]
        return domain

    @api.onchange("project_id")
    def onchange_project_id(self):
        """
        Override the onchange method to update the domain of `task_id` dynamically.
        """
        res = super(AccountAnalyticLine, self).onchange_project_id()

        if self.project_id:
            res = res or {"domain": {}}
            res["domain"].update({"task_id": self._task_domain()})

        return res

    @api.model
    def _get_task_domain(self):
        return (
            "["
            "('project_id', '=', project_id),"
            "('stage_id.allow_timesheet', '=', True),"
            "('stage_id.closed', '=', False)"
            "]"
        )
