# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollPreparationLine(models.Model):

    _inherit = 'payroll.preparation.line'

    prorata = fields.Float(default=1)
    prorata_amount = fields.Float(compute="_compute_prorata_amount", store=True)

    @api.depends("prorata", "amount")
    def _compute_prorata_amount(self):
        for line in self:
            line.prorata_amount = line.prorata * line.amount
