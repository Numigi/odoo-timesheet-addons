# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):

    _inherit = "project.project"

    @api.constrains("parent_id")
    def _check_cannot_change_parent_while_existing_timesheet(self):
        analytic_line_env = self.env["account.analytic.line"]
        for project in self:
            if analytic_line_env.search([("project_id", "=", project.id)], limit=1):
                raise ValidationError(
                    _(
                        "Timesheet already exists on this project, to update the Parent "
                        "Project field, the Project "
                        "must have no Timesheets."
                    )
                )
