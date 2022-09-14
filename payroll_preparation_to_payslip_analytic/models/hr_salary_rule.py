# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    propagate_account_debit = fields.Boolean(
        "Propagate Payroll Entries Analytic Account (Debit)"
    )
    propagate_account_credit = fields.Boolean(
        "Propagate Payroll Entries Analytic Account (Credit)"
    )
