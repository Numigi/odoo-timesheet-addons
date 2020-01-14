# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PayrollPreparationLine(models.Model):

    _name = 'payroll.preparation.line'
    _description = 'Payroll Entry'
    _order = 'date'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    period_id = fields.Many2one(
        'payroll.period',
        index=True,
        ondelete='restrict',
        track_visibility="onchange",
    )
    week = fields.Integer(
        compute='_compute_week',
        store=True,
        index=True,
    )
    date = fields.Date(
        track_visibility="onchange",
    )
    employee_id = fields.Many2one(
        'hr.employee',
        required=True,
        index=True,
        ondelete='restrict',
        track_visibility="onchange",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        ondelete='restrict',
        track_visibility="onchange",
    )
    code = fields.Char(
        track_visibility="onchange",
    )
    duration = fields.Float(
        track_visibility="onchange",
    )
    amount = fields.Float(
        track_visibility="onchange",
    )

    @api.depends('period_id', 'date')
    def _compute_week(self):
        lines_with_period = self.filtered(lambda l: l.period_id)
        for line in lines_with_period:
            number_of_days = (line.date - line.period_id.date_from).days
            line.week = (number_of_days // 7) + 1
