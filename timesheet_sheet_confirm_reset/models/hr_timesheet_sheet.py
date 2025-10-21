# Copyright Numigi 2025 (tm) and all its contributors
# (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet.sheet'

    def action_confirm_reset(self):
        """
        Allow the owner (employee's user) to reset a submitted sheet back to draft,
        provided it is not approved. Raises errors if the sheet is already approved
        or modified concurrently.
        """
        self.ensure_one()
        current_uid = self.env.uid
        if (
            self.user_id.id != current_uid
            and not self.env.user.has_group('hr_timesheet.group_hr_timesheet_user')
        ):
            raise UserError(_('You can only reset your own timesheets.'))

        timesheet_id = self.with_context(prefetch_fields=False).sudo().browse(self.id)
        if not timesheet_id:
            raise UserError(_('Timesheet not found.'))

        if timesheet_id.state == 'done':
            raise UserError(_('Error: You cannot reset a timesheet that has already '
                              'been approved.'))

        if timesheet_id.state in ('draft', False):
            raise UserError(_('The timesheet is already in draft state.'))

        timesheet_id.sudo().write({'state': 'draft'})
