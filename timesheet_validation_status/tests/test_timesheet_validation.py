# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import AccessError
from odoo.tests import common


class TestTimesheetValidation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_group = cls.env.ref('hr_timesheet.group_hr_timesheet_user')
        cls.manager_group = cls.env.ref('hr_timesheet.group_timesheet_manager')

        cls.user = cls.env.ref('base.user_demo')

        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
        })
        cls.task = cls.env['project.task'].create({
            'name': 'My Task',
            'project_id': cls.project.id,
        })
        cls.line_1 = cls.env['account.analytic.line'].create({
            'name': '/',
            'project_id': cls.project.id,
            'task_id': cls.task.id,
            'user_id': cls.user.id,
        })
        cls.line_2 = cls.env['account.analytic.line'].create({
            'name': '/',
            'project_id': cls.project.id,
            'task_id': cls.task.id,
            'user_id': cls.user.id,
        })

    def test_manager_can_validate_timesheets(self):
        self.user.groups_id |= self.manager_group
        self.line_1.sudo(self.user).validate_timesheet_entries()
        assert self.line_1.validated_timesheet

    def test_user_can_not_validate_timesheets(self):
        self.user.groups_id |= self.user_group
        with pytest.raises(AccessError):
            self.line_1.sudo(self.user).validate_timesheet_entries()

    def test_validate_multiple_timesheets(self):
        (self.line_1 | self.line_2).validate_timesheet_entries()
        assert self.line_1.validated_timesheet
        assert self.line_2.validated_timesheet

    def test_timesheet_can_be_validated_multiple_times(self):
        self.line_1.validate_timesheet_entries()
        self.line_1.validate_timesheet_entries()
        assert self.line_1.validated_timesheet

    def test_user_can_not_change_the_validation_status(self):
        with pytest.raises(AccessError):
            self.line_1.sudo(self.user).write({'validated_timesheet': True})

    def test_user_can_not_create_a_validated_timesheet(self):
        with pytest.raises(AccessError):
            self.line_1.sudo(self.user).copy({'validated_timesheet': True})

    def test_if_not_timesheet_line__can_not_validate_line(self):
        self.line_1.project_id = False
        with pytest.raises(AccessError):
            self.line_1.validate_timesheet_entries()

    def test_if_not_manager__can_not_modify_validated_timesheet(self):
        self.line_1.validated_timesheet = True
        with pytest.raises(AccessError):
            self.line_1.sudo(self.user).write({'name': 'Some Value'})

    def test_if_manager__can_modify_validated_timesheet(self):
        self.line_1.validated_timesheet = True
        self.user.groups_id |= self.manager_group
        self.line_1.sudo(self.user).write({'name': 'Some Value'})
