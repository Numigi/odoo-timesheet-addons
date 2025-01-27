# Copyright 2023-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _check_can_update_timesheet(self):
        if self.env.context.get("holidays_time_control"):
            return True
        return super(AccountAnalyticLine, self)._check_can_update_timesheet()
