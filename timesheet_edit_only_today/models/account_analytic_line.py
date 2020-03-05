# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo import models, _
from odoo.exceptions import AccessError

PAST_FUTURE_DATE_ERROR_MESSAGE = _(
    "You are not allowed to edit, create or delete timesheet entries "
    "for past or future dates."
)


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
        for line in self:
            self.check_is_not_past_or_future_date(line.date)

    def check_is_not_past_or_future_date(self, date):
        today = datetime.now().date()
        is_past_or_future_date = date != today
        if is_past_or_future_date:
            raise AccessError(PAST_FUTURE_DATE_ERROR_MESSAGE)
