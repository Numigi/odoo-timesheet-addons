# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import fields, models, _
from odoo.exceptions import AccessError

DEFAULT_FILE_NAME = _('No Content.txt')
DEFAULT_FILE_CONTENT = _(
    "Your payroll preparation export file could not be generated.\n\n"
    "Make sure you have installed the proper extension to generate "
    "the file in the format expected by your payroll system."
)


class PayrollPreparationExport(models.TransientModel):

    _name = 'payroll.preparation.export'
    _description = 'Export Payroll Preparation Entries'

    period_id = fields.Many2one(
        'payroll.period',
    )
    file = fields.Binary()
    filename = fields.Char()

    def action_validate(self):
        lines = self.get_payroll_preparation_lines()
        self.generate_file(lines)
        self.create_history_entry()
        return self.get_wizard_action()

    def get_wizard_action(self):
        action = self.get_formview_action()
        action['target'] = 'new'
        return action

    def get_payroll_preparation_lines(self):
        return self.env['payroll.preparation.line'].search([
            ('period_id', '=', self.period_id.id),
        ])

    def generate_file(self, lines):
        self.filename = _(DEFAULT_FILE_NAME)
        self.file = base64.b64encode(_(DEFAULT_FILE_CONTENT).encode('utf-8'))

    def create_history_entry(self):
        return self.sudo().env['payroll.preparation.export.history'].create({
            'period_id': self.period_id.id,
            'file': self.file,
            'filename': self.filename,
            'user_id': self.env.user.id,
        })
