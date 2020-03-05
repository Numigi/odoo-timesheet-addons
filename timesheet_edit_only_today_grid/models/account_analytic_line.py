# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo import fields, models


class TimesheetEntry(models.Model):

    _inherit = 'account.analytic.line'

    def adjust_grid(self, row_domain, column_field, column_value, cell_field, change):
        result = super().adjust_grid(
            row_domain, column_field, column_value, cell_field, change
        )

        if not self._user_can_edit_past_future_timesheets():
            date_str = column_value.split('/')[0]
            date_ = fields.Date.from_string(date_str)
            self.check_is_not_past_or_future_date(date_)

        return result
