# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class PayrollEntry(models.Model):
    _inherit = "payroll.preparation.line"

    project_id = fields.Many2one(
        'project.project',
        'Project',
        ondelete="restrict",
        track_visibility="onchange",
    )

    def open_payslip_wizard(self):
        self._check_project_id()
        return super(PayrollEntry, self).open_payslip_wizard()

    def _check_project_id(self):
        if len(self.mapped('project_id')) > 1:
            raise ValidationError(_(
                "You can only process Entries from a "
                "single project at a time."))
