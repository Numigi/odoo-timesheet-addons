# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    payroll_preparation_line_ids = fields.One2many(
        'payroll.preparation.line',
        'timesheet_id',
        'Payroll Entries',
    )

    @api.multi
    def unlink(self):
        for line in self:
            if line._has_payroll_entries():
                raise ValidationError(_(
                    "You may not delete the timesheet line {} "
                    "because it is linked to a payroll entry."
                ).format(line.display_name))
        return super().unlink()

    @api.multi
    def write(self, vals):
        is_super_admin = self.env.user._is_superuser()
        if not is_super_admin:
            self._check_protected_vals_for_payroll_entries(vals)
        return super().write(vals)

    def _check_protected_vals_for_payroll_entries(self, vals):
        protected_fields = self._get_payroll_entry_protected_fields()
        protected_field_modified = protected_fields.intersection(vals)
        for line in self:
            if protected_field_modified and line._has_payroll_entries():
                raise ValidationError(_(
                    "You may not modify the timesheet line {} "
                    "because it is linked to a payroll entry."
                ).format(line.display_name))

    def _get_payroll_entry_protected_fields(self):
        return {
            'account_id',
            'company_id',
            'date',
            'employee_id',
            'name',
            'payroll_period_id',
            'project_id',
            'task_id',
            'unit_amount',
        }

    def _has_payroll_entries(self):
        return bool(self.sudo().payroll_preparation_line_ids)
