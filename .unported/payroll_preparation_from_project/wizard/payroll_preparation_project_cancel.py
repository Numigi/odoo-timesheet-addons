# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import AccessError


class PayrollPreparationProjectCancel(models.TransientModel):

    _name = 'payroll.preparation.project.cancel'
    _description = 'Generate Payroll Entries Project Cancel'

    project_ids = fields.Many2many(
        "project.project",
        "payroll_preparation_project_cancel_rel",
        "wizard_id",
        "project_id",
        "Projects",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_ids = self._context.get("active_ids") or []
        res["project_ids"] = [(6, 0, active_ids)]

        return res

    def action_validate(self):
        self.project_ids.cancel_payroll_entries()
