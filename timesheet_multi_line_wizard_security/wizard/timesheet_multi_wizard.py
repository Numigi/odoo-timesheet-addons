# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class TimesheetMultiWizard(models.TransientModel):

    _inherit = 'timesheet.multi.wizard'

    def _create_timesheet_entries(self):
        super()._create_timesheet_entries()
        timesheet_lines = self.mapped('line_ids.timesheet_line_id')
        timesheet_lines.check_extended_security_create()
        timesheet_lines.check_extended_security_all()
