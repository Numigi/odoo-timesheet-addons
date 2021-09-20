# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, _
from odoo.exceptions import AccessError


class PayrollPreparationFromProject(models.TransientModel):

    _name = 'payroll.preparation.from.project'
    _description = 'Generate Payroll Entries From Project'

    project_id = fields.Many2one("project.project")
    period_id = fields.Many2one('payroll.period')

    def action_validate(self):
        pass
