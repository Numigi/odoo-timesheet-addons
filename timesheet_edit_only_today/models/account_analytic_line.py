# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo import models, _
from odoo.exceptions import AccessError


class TimesheetEntry(models.Model):

    _inherit = 'account.analytic.line'

    def check_extended_security_write(self):
        super().check_extended_security_write()
        if not self._user_can_edit_past_future_timesheets():
            self._check_is_current_date_timesheet()

    def check_extended_security_create(self):
        super().check_extended_security_create()
        if not self._user_can_edit_past_future_timesheets():
            self._check_is_current_date_timesheet()

    def check_extended_security_unlink(self):
        super().check_extended_security_unlink()
        if not self._user_can_edit_past_future_timesheets():
            self._check_is_current_date_timesheet()

    def _user_can_edit_past_future_timesheets(self):
        return self.env.user.has_group('hr_timesheet.group_timesheet_manager')

    def _check_is_current_date_timesheet(self):
        today = datetime.now().date()
        non_current_timesheets = self.filtered(lambda l: l.project_id and l.date != today)
        if non_current_timesheets:
            raise AccessError(_(
                "You are not allowed to edit, create or delete timesheet entries "
                "for past or future dates."
            ))
