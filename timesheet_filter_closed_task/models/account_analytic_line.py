# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    task_id = fields.Many2one(
        domain=lambda self: self._get_task_domain(),
    )
    
    def _get_task_domain(self):
        return [
            ('stage_id.closed', '=', False),
            ('project_id', '=', 'project_id'),
            ('stage_id.allow_timesheet', '=', True),
        ]