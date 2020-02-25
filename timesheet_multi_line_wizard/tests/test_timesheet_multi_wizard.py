# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TimesheetMultiLineCase


class TestTimesheetMultiLine(TimesheetMultiLineCase):

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
        new_line = self.get_employee_timesheets(self.employee)
        assert len(new_line) == 1
        assert new_line.project_id == self.project
        assert new_line.date == self.yesterday
        assert new_line.task_id == self.task
        assert new_line.name == self.description
        assert new_line.user_id == self.user
        assert new_line.unit_amount == self.time_spent

    def test_save_with_2_lines(self):
        self.wizard.line_ids |= self.new_wizard_line(
            self.task, self.description, self.time_spent)
        self.wizard.action_save()
        new_lines = self.get_employee_timesheets(self.employee)
        assert len(new_lines) == 2

    def test_save_and_new(self):
        self.wizard.action_save_and_new()
        new_line = self.get_employee_timesheets(self.employee)
        assert len(new_line) == 1

    def test_after_save_and_new__new_wizard_opened(self):
        action = self.wizard.action_save_and_new()
        assert action['res_model'] == 'timesheet.multi.wizard'
        assert action['target'] == 'new'

    def test_after_save_and_new__new_wizard_has_same_parameters(self):
        action = self.wizard.action_save_and_new()
        new_wizard = self.get_wizard_from_action(action)
        assert new_wizard != self.wizard
        assert new_wizard.project_id == self.project
        assert new_wizard.employee_id == self.employee
        assert new_wizard.date == self.yesterday

    def test_if_employee_has_same_company__employee_in_default_value(self):
        defaults = self.get_wizard_default_values(self.user)
        assert defaults['employee_id'] == self.employee.id

    def test_if_employee_has_not_same_company__employee_not_in_default_value(self):
        new_company = self.env['res.company'].create({'name': 'New Company'})
        self.employee.company_id = new_company
        defaults = self.get_wizard_default_values(self.user)
        assert not defaults['employee_id']
