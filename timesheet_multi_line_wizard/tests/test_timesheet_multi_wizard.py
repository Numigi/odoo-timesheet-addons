# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests import common


class TestTimesheetPayrollPeriod(common.SavepointCase):

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

        cls.wizard = cls._create_wizard(cls.project, cls.employee, cls.yesterday)
        cls.wizard.line_ids = cls._new_wizard_line(cls.task, cls.description, cls.time_spent)

    def test_onchange_project__if_not_project__lines_deleted(self):
        with self.env.do_in_onchange():
            self.wizard.project_id = False
            self.wizard._onchange_project_id()

        assert not self.wizard.line_ids

    def test_onchange_project__if_other_project__lines_deleted(self):
        with self.env.do_in_onchange():
            self.wizard.project_id = self.project_2
            self.wizard._onchange_project_id()

        assert not self.wizard.line_ids

    def test_onchange_project__if_other_project__lines_not_deleted(self):
        with self.env.do_in_onchange():
            self.wizard._onchange_project_id()

        assert len(self.wizard.line_ids) == 1

    def test_save(self):
        self.wizard.action_save()
        new_line = self._get_employee_timesheets(self.employee)
        assert len(new_line) == 1
        assert new_line.project_id == self.project
        assert new_line.date == self.yesterday
        assert new_line.task_id == self.task
        assert new_line.name == self.description
        assert new_line.user_id == self.user
        assert new_line.unit_amount == self.time_spent

    def test_save_with_2_lines(self):
        self.wizard.line_ids |= self._new_wizard_line(
            self.task, self.description, self.time_spent)
        self.wizard.action_save()
        new_lines = self._get_employee_timesheets(self.employee)
        assert len(new_lines) == 2

    def test_save_and_new(self):
        self.wizard.action_save_and_new()
        new_line = self._get_employee_timesheets(self.employee)
        assert len(new_line) == 1

    def test_after_save_and_new__new_wizard_opened(self):
        action = self.wizard.action_save_and_new()
        assert action['res_model'] == 'timesheet.multi.wizard'
        assert action['target'] == 'new'

    def test_after_save_and_new__new_wizard_has_same_parameters(self):
        action = self.wizard.action_save_and_new()
        new_wizard = self._get_wizard_from_action(action)
        assert new_wizard != self.wizard
        assert new_wizard.project_id == self.project
        assert new_wizard.employee_id == self.employee
        assert new_wizard.date == self.yesterday

    def test_if_employee_has_same_company__employee_in_default_value(self):
        defaults = self._get_wizard_default_values(self.user)
        assert defaults['employee_id'] == self.employee.id

    def test_if_employee_has_not_same_company__employee_not_in_default_value(self):
        new_company = self.env['res.company'].create({'name': 'New Company'})
        self.employee.company_id = new_company
        defaults = self._get_wizard_default_values(self.user)
        assert not defaults['employee_id']

    @classmethod
    def _get_wizard_default_values(cls, user):
        wizard_obj = cls.env['timesheet.multi.wizard']
        fields = list(wizard_obj._fields)
        return wizard_obj.sudo(user).default_get(fields)

    @classmethod
    def _create_wizard(cls, project, employee, date_):
        return cls.env['timesheet.multi.wizard'].create({
            'project_id': project.id,
            'employee_id': employee.id,
            'date': date_,
        })

    @classmethod
    def _new_wizard_line(cls, task, description, time_spent):
        return cls.env['timesheet.multi.wizard.line'].new({
            'task_id': task.id,
            'description': description,
            'time_spent': time_spent,
        })

    @classmethod
    def _get_employee_timesheets(cls, employee):
        return cls.env['account.analytic.line'].search([
            ('employee_id', '=', employee.id),
        ])

    @classmethod
    def _get_wizard_from_action(cls, action):
        wizard_id = action['res_id']
        return cls.env['timesheet.multi.wizard'].browse(wizard_id)
