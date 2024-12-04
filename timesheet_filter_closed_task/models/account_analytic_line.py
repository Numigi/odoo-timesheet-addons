# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.model
    def _get_task_domain(self):
        return "[" \
               "('project_id', '=', project_id)," \
               "('stage_id.allow_timesheet', '=', True)," \
                "('stage_id.closed', '=', False)," \
               "]"
