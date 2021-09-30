# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollPreparationLine(models.Model):

    _name = "payroll.preparation.line"
    _description = "Payroll Entry"
    _order = "date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    period_id = fields.Many2one(
        "payroll.period",
        index=True,
        ondelete="restrict",
        track_visibility="onchange",
    )
    week_number = fields.Integer(
        compute="_compute_week_number",
        store=True,
        index=True,
    )
    date = fields.Date(
        track_visibility="onchange",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        required=True,
        index=True,
        ondelete="restrict",
        track_visibility="onchange",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        ondelete="restrict",
        track_visibility="onchange",
    )
    code = fields.Char(
        track_visibility="onchange",
    )
    duration = fields.Float(
        track_visibility="onchange",
    )
    hourly_rate = fields.Float(
        track_visibility="onchange",
    )
    amount = fields.Float(
        track_visibility="onchange",
    )

    def name_get(self):
        return [(l.id, l._get_display_name()) for l in self]

    def _get_display_name(self):
        parts = []

        if self.date:
            parts.append(str(self.date))

        parts.append(self.employee_id.display_name)

        if self.code:
            parts.append(self.code)

        return " - ".join(parts)

    @api.depends("period_id", "date")
    def _compute_week_number(self):
        lines_with_date_and_period = self.filtered(lambda l: l.date and l.period_id)

        for line in lines_with_date_and_period:
            number_of_days = (line.date - line.period_id.date_from).days
            line.week_number = (number_of_days // 7) + 1

    @api.constrains("date", "period_id")
    def _check_date_matches_period(self):
        lines_with_date_and_period = self.filtered(lambda l: l.date and l.period_id)

        for line in lines_with_date_and_period:
            period = line.period_id
            date_matches_period = period.date_from <= line.date <= period.date_to

            if not date_matches_period:
                raise ValidationError(
                    _(
                        "The selected date ({date}) does not match the period ({period}) "
                        "for the payroll entry {entry}."
                    ).format(
                        date=line.date,
                        period=period.display_name,
                        entry=line.display_name,
                    )
                )
