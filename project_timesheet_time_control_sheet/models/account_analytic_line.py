# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    def unlink(self):
        lines_with_zero = self.filtered(lambda l: not l.unit_amount)
        other_lines = self - lines_with_zero
        super(
            AnalyticLine, lines_with_zero.with_context(skip_check_state=True)
        ).unlink()
        super(AnalyticLine, other_lines).unlink()
        return True
