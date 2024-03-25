# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountAnalyticLine(models.Model):
    _name = "account.analytic.line"
    _inherit = ["account.analytic.line", "mail.thread", "mail.activity.mixin"]
