# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date
from odoo import api, fields, models


def _recompute_timesheet_periods(env: 'Environment', date_from: date, date_to: date):
    """Recompute the period of timesheets for a given range of dates."""
    timesheets_to_recompute = env['account.analytic.line'].sudo().search([
        ('date', '>=', date_from),
        ('date', '<=', date_to),
        ('project_id', '!=', False),
    ])
    timesheets_to_recompute.update({'payroll_period_id': False})
    timesheets_to_recompute._compute_payroll_period_id()


class PayrollPeriod(models.Model):

    _inherit = 'payroll.period'

    @api.model
    def create(self, vals):
        """When a period is created, recompute relevant timesheet entries."""
        period = super().create(vals)
        _recompute_timesheet_periods(self.env, period.date_from, period.date_to)
        return period

    @api.multi
    def write(self, vals):
        """When a period is changed, recompute relevant timesheet entries.

        The timesheets to recompute are those included inside
        the time range before and after the write operation.
        """
        min_date_before = min(p.date_from for p in self)
        max_date_before = max(p.date_to for p in self)
        super().write(vals)
        min_date = min(min_date_before, min(p.date_from for p in self))
        max_date = max(max_date_before, max(p.date_to for p in self))
        _recompute_timesheet_periods(self.env, min_date, max_date)
        return True
