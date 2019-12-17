# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TimesheetEntry(models.Model):

    _inherit = 'account.analytic.line'

    payroll_period_id = fields.Many2one(
        'payroll.period',
        'Payroll Period',
        compute='_compute_payroll_period_id',
        index=True,
        store=True,
    )

    @api.depends('date', 'company_id', 'project_id')
    def _compute_payroll_period_id(self):
        """Compute the payroll period.

        Because finding a period implies a search operations
        with multiple SELECT queries, a cache is used to compute
        the field for multiple timesheet entries.
        """
        timesheet_lines = self.filtered(lambda l: l.project_id)

        period_cache = {}

        for line in timesheet_lines:
            index = (line.date, line.company_id)

            if index not in period_cache:
                period_cache[index] = self.env['payroll.period'].find_period(*index)

            line.payroll_period_id = period_cache[index]

    payroll_period_date_from = fields.Date(
        string="Payroll Period Start Date",
        related='payroll_period_id.date_from',
        store=True,
    )

    payroll_period_date_to = fields.Date(
        string="Payroll Period End Date",
        related='payroll_period_id.date_to',
        store=True,
    )

    payroll_period_week = fields.Integer(
        string="Payroll Period Week",
        compute='_compute_payroll_period_week',
        store=True,
    )

    @api.depends('payroll_period_id', 'date')
    def _compute_payroll_period_week(self):
        lines_with_period = self.filtered(lambda l: l.payroll_period_id)

        for line in lines_with_period:
            number_of_days = (line.date - line.payroll_period_id.date_from).days
            line.payroll_period_week = (number_of_days // 7) + 1
