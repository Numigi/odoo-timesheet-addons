# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PayrollEntry(models.Model):

    _inherit = "payroll.preparation.line"

    payslip_id = fields.Many2one("hr.payslip", index=True, ondelete="restrict")
