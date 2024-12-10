# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    project_id = fields.Many2one(string="Iteration")
    parent_project_id = fields.Many2one(
        "project.project",
        "Parent Project",
        compute="_compute_parent_project_id",
        store=True,
        index=True,
        compute_sudo=True,
    )

    @api.depends("project_id", "project_id.child_ids_count", "project_id.parent_id")
    def _compute_parent_project_id(self):
        """
        Compute the parent project of an analytic line.
        If the project has no parent, then the parent
        project is the project itself.
        """
        for line in self:
            line.parent_project_id = (
                line.project_id.parent_id
                if line.project_id.parent_id
                else line.project_id
            )
