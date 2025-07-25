# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PayrollPreparationLine(models.Model):

    _inherit = 'payroll.preparation.line'

    timesheet_id = fields.Many2one(
        'account.analytic.line',
        ondelete='restrict',
        index=True,
    )
