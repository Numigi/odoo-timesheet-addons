# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollPeriod(models.Model):

    _name = 'payroll.period'
    _description = 'Payroll Period'
    _order = 'date_from desc'

    name = fields.Char(compute='_compute_name', store=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    active = fields.Boolean(default=True)

    @api.depends('date_from', 'date_to')
    def _compute_name(self):
        for period in self:
            period.name = "{} / {}".format(period.date_from, period.date_to)

    def _find_overlapping_periods(self):
        all_periods = self.search([
            ('id', '!=', self.id),
            ('company_id', '=', self.company_id.id),
        ])
        return all_periods.filtered(
            lambda p: self.date_from <= p.date_from <= self.date_to or
            self.date_from <= p.date_to <= self.date_to
        )

    @api.constrains('date_from', 'date_to', 'company_id', 'active')
    def check_no_overlapping_period(self):
        for period in self:
            overlapping_periods = period._find_overlapping_periods()
            if overlapping_periods:
                raise ValidationError(_(
                    'Another period ({period}) is overlapping the selected date range.'
                ).format(period=overlapping_periods[0].display_name))

    def find_period(self, date_, company):
        """Find a period for the given date and company.

        :param date_: the date for which to find the period
        :param company: the company for which to find the period
        :return: a single matching period if any found, otherwise a null recordset
        """
        return self.env['payroll.period'].search([
            ('date_from', '<=', date_),
            ('date_to', '>=', date_),
            ('company_id', '=', company.id),
        ], limit=1)
