# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class TimesheetMultiWizard(models.TransientModel):

    _name = 'timesheet.multi.wizard'
    _description = 'Timesheet Multi Wizard'

    def _get_user_employee(self):
        user = self.env.user
        employees = user.employee_ids.sudo()
        employees_with_same_company = employees.filtered(lambda e: e.company_id == user.company_id)
        return employees_with_same_company[0] if employees_with_same_company else None

    project_id = fields.Many2one(
        'project.project',
        required=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        required=True,
        default=_get_user_employee,
    )
    date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )

    line_ids = fields.One2many(
        'timesheet.multi.wizard.line',
        'wizard_id',
    )

    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.line_ids = self.line_ids.filtered(
            lambda l: l.task_id.project_id == self.project_id)

    def action_save(self):
        self._create_timesheet_entries()

    def action_save_and_new(self):
        self._create_timesheet_entries()

        new_wizard = self.copy()
        return new_wizard.get_wizard_open_action()

    def _create_timesheet_entries(self):
        for line in self.line_ids:
            line._create_timesheet_entry()

    def get_wizard_open_action(self):
        action = self.get_formview_action()
        action['name'] = _('New Timesheets')
        action['target'] = 'new'
        return action


class TimesheetMultiWizardLine(models.TransientModel):

    _name = 'timesheet.multi.wizard.line'
    _description = 'Timesheet Multi Wizard Line'

    wizard_id = fields.Many2one(
        'timesheet.multi.wizard',
        required=True,
        ondelete='cascade',
    )
    task_id = fields.Many2one(
        'project.task',
        required=True,
    )
    description = fields.Text()
    time_spent = fields.Float(required=True)

    def _create_timesheet_entry(self):
        vals = self._get_timesheet_vals()
        self.env['account.analytic.line'].create(vals)

    def _get_timesheet_vals(self):
        wizard = self.wizard_id
        return {
            'project_id': wizard.project_id.id,
            'employee_id': wizard.employee_id.id,
            'date': wizard.date,
            'user_id': wizard.employee_id.user_id.id,
            'name': self.description,
            'task_id': self.task_id.id,
            'unit_amount': self.time_spent,
        }
