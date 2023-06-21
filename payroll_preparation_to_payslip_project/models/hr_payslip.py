# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    project_id = fields.Many2one(
        'project.project',
        'Project',
        ondelete="restrict"
    )

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for record in self:
            if record.move_id and record.move_id.line_ids:
                record.move_id.line_ids.write({
                    'project_id': record.project_id.id,
                })
        return res


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    project_id = fields.Many2one(
        'project.project',
        'Project',
        related="slip_id.project_id",
        store=True,
    )
