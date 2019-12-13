# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class TimesheetEntry(models.Model):

    _inherit = 'account.analytic.line'

    validated_timesheet = fields.Boolean(
        'Validated Timesheet',
        copy=False,
        readonly=True,
    )

    def check_timesheet_validation_access(self):
        """Check whether or not the user is allowed to validate the timesheets.

        This method is intended to be inherited in other modules to add
        specific validation checks.

        By default, only the timesheet manager is allowed to validate timesheets.
        """
        if not self.env.user.has_group('hr_timesheet.group_timesheet_manager'):
            raise AccessError(_(
                'You are not authorized to validate timesheets.'
            ))

    def validate_timesheet_entries(self):
        self.check_timesheet_validation_access()
        lines_without_project = self.filtered(lambda l: not l.project_id)
        if lines_without_project:
            raise AccessError(_(
                'Some analytic lines selected for validation are not timesheets: '
                '\n\n'
                '{lines}'
            ).format(lines='\n'.join(lines_without_project.mapped('display_name'))))

        self.sudo().write({'validated_timesheet': True})

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line.validated_timesheet:
            line.check_timesheet_validation_access()
        return line

    def check_validated_timesheet_write_access(self):
        """Check whether or not the user is allowed to modify a validated timesheets.

        This method is intended to be inherited in other modules to add
        specific validation checks.

        By default, only the timesheet manager is allowed to validate timesheets.
        """
        if not self.env.user.has_group('hr_timesheet.group_timesheet_manager'):
            raise AccessError(_(
                'You are not authorized to modify a validated timesheet.'
            ))

    @api.multi
    def write(self, vals):
        validated_timesheets = self.filtered(lambda t: t.validated_timesheet)
        if validated_timesheets:
            validated_timesheets.check_validated_timesheet_write_access()

        super().write(vals)
        if vals.get('validated_timesheet') and not self.env.user._is_superuser():
            self.check_timesheet_validation_access()
        return True
