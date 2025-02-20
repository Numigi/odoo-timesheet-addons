# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):

    _inherit = "project.project"

    is_parent_editable = fields.Boolean(
        string="Allow Parent Project Edit",
        help="""If checked, allows modifying the parent project even
        if there are existing timesheet lines.""",
    )

    @api.constrains("parent_id")
    def _check_cannot_change_parent_while_existing_timesheet(self):
        analytic_line = self.env["account.analytic.line"]
        for project in self:
            if not project.is_parent_editable and analytic_line.search(
                [("project_id", "=", project.id)], limit=1
            ):
                raise ValidationError(
                    _(
                        "Timesheet already exists on this project, to update the Parent "
                        "Project field, the Project must have no Timesheets."
                    )
                )
