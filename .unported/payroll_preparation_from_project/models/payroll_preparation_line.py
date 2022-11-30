# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PayrollEntry(models.Model):

    _inherit = "payroll.preparation.line"

    project_id = fields.Many2one("project.project", index=True, ondelete="restrict")

    @api.onchange("project_id")
    def _onchange_project_id(self):
        self.analytic_account_id = self.project_id.analytic_account_id
