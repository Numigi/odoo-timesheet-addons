# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests import common


class TimesheetMultiLineCase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'User A',
            'email': 'usera@test.com',
            'login': 'usera@test.com',
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Employee A',
            'user_id': cls.user.id,
        })

        cls.company = cls.env['res.company'].create({'name': 'Company A'})

        cls.yesterday = datetime.now().date() - timedelta(1)

        cls.project = cls.env['project.project'].create({
            'name': 'Project 1',
            'company_id': cls.company.id,
        })

        cls.project_2 = cls.env['project.project'].create({
            'name': 'Project 2',
            'company_id': cls.company.id,
        })

        cls.task = cls.env['project.task'].create({
            'name': 'Task 1',
            'project_id': cls.project.id,
        })
        cls.time_spent = 1
        cls.description = 'Timesheet description 1'

        cls.wizard = cls.create_wizard(cls.project, cls.employee, cls.yesterday)
        cls.wizard.line_ids = cls.new_wizard_line(cls.task, cls.description, cls.time_spent)

    @classmethod
    def get_wizard_default_values(cls, user):
        wizard_obj = cls.env['timesheet.multi.wizard']
        fields = list(wizard_obj._fields)
        return wizard_obj.sudo(user).default_get(fields)

    @classmethod
    def create_wizard(cls, project, employee, date_):
        return cls.env['timesheet.multi.wizard'].create({
            'project_id': project.id,
            'employee_id': employee.id,
            'date': date_,
        })

    @classmethod
    def new_wizard_line(cls, task, description, time_spent):
        return cls.env['timesheet.multi.wizard.line'].new({
            'task_id': task.id,
            'description': description,
            'time_spent': time_spent,
        })

    @classmethod
    def get_employee_timesheets(cls, employee):
        return cls.env['account.analytic.line'].search([
            ('employee_id', '=', employee.id),
        ])

    @classmethod
    def get_wizard_from_action(cls, action):
        wizard_id = action['res_id']
        return cls.env['timesheet.multi.wizard'].browse(wizard_id)
