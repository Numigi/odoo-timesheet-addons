# Copyright 2023-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def action_validate(self):
        res = super().action_validate()
        for holiday in self:
            if holiday.timesheet_ids:
                for timesheet_line in holiday.timesheet_ids:
                    timesheet_line.date_time = datetime.datetime.combine(
                        timesheet_line.date, datetime.time(8, 00)
                    )
        return res
