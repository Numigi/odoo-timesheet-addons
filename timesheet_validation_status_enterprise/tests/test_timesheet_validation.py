# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestTimesheetValidation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        })

    def test_field_validated_is_based_on_field_validated_timesheet(self):
        assert not self.line_1.validated
        self.line_1.validate_timesheet_entries()
        assert self.line_1.validated
