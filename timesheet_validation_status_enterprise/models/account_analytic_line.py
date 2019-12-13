# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class TimesheetEntry(models.Model):

    _inherit = 'account.analytic.line'

    @api.depends('validated_timesheet')
    def _compute_timesheet_validated(self):
        for line in self:
            line.validated = line.validated_timesheet
