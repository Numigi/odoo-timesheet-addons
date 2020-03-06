# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PayrollPreparationExportHistory(models.Model):

    _name = 'payroll.preparation.export.history'
    _description = 'Payroll Preparation Export History'
    _order = 'id desc'
    _rec_name = 'filename'

    company_id = fields.Many2one(
        related='period_id.company_id',
        store=True
    )
    user_id = fields.Many2one(
        'res.users',
    )
    period_id = fields.Many2one(
        'payroll.period',
        required=True,
        index=True,
    )
    file = fields.Binary()
    filename = fields.Char()
