# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PayrollPreparationFromTimesheet(models.TransientModel):

    _name = 'payroll.preparation.from.timesheet'
    _description = 'Generate Payroll Entries From Timesheet'

    period_id = fields.Many2one('payroll.period')

    def action_validate(self):
        self._remove_existing_payroll_entries()
        self._generate_payroll_entries()

    def _remove_existing_payroll_entries(self):
        """Remove existing (deprecated) payroll entries."""
        entries_to_remove = self.env['payroll.preparation.line'].search([
            ('period_id', '=', self.period_id.id),
            ('timesheet_id', '!=', False),
        ])
        entries_to_remove.unlink()

    def _generate_payroll_entries(self):
        timesheets = self._find_timesheets_to_process()

        for timesheet in timesheets:
            self._process_timesheet_line(timesheet)

    def _find_timesheets_to_process(self):
        return self.env['account.analytic.line'].search([
            ('payroll_period_id', '=', self.period_id.id),
            ('project_id', '!=', False),
        ])

    def _process_timesheet_line(self, timesheet):
        self._generate_salary_entry(timesheet)

    def _generate_salary_entry(self, timesheet):
        vals = self._get_salary_entry_vals(timesheet)
        self.env['payroll.preparation.line'].create(vals)

    def _get_salary_entry_vals(self, timesheet):
        """Get values a salary (hourly) payroll entry.

        The amount is left to 0.
        This module does not define how the hourly rate is computed.
        """
        vals = self._get_common_entry_vals(timesheet)
        vals['duration'] = timesheet.unit_amount
        vals['amount'] = 0
        return vals

    def _get_common_entry_vals(self, timesheet):
        """Get values common for any payroll entry generated from a timesheet line."""
        return {
            'analytic_account_id': timesheet.account_id.id,
            'company_id': timesheet.company_id.id,
            'date': timesheet.date,
            'employee_id': timesheet.employee_id.id,
            'period_id': self.period_id.id,
            'timesheet_id': timesheet.id,
        }
