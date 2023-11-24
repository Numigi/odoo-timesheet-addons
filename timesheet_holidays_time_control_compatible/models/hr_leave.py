# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _timesheet_prepare_line_values(self, index, work_hours_data, day_date, work_hours_count):
        self.ensure_one()
        timesheet_line = super()._timesheet_prepare_line_values(
            index, work_hours_data, day_date, work_hours_count)
        timesheet_line["date_time"] = datetime.datetime.combine(
            day_date, datetime.time(8, 00))
        return timesheet_line
