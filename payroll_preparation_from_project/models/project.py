# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _


class Project(models.Model):

    _inherit = "project.project"

    def open_payroll_preparation_wizard(self):
        action = self.env["payroll.preparation.from.project"].get_formview_action()
        action["target"] = "new"
        action["context"] = {
            "default_project_id": self.id,
        }
        return action

    def view_payroll_entries(self):
        return {
            "name": _("Payroll Entries"),
            "type": "ir.actions.act_window",
            "res_model": "payroll.preparation.line",
            "view_type": "form",
            "view_mode": "list,form",
            "target": "current",
            "context": {
                "search_default_project_id": self.id,
            },
        }
