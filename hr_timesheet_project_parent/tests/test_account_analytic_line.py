# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectIterationWithTimeSheet(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env["project.project"].create({"name": "Project 1"})
        cls.project_2 = cls.env["project.project"].create({"name": "Project 2"})

        cls.iteration_1 = cls.env["project.project"].create(
            {
                "name": "Iteration 1",
                "parent_id": cls.project_1.id,
            }
        )
        cls.iteration_2 = cls.env["project.project"].create(
            {
                "name": "Iteration 2",
                "parent_id": cls.project_1.id,
            }
        )

    def _create_timesheet(self, project):

        return self.env["account.analytic.line"].create(
            {
                "name": "Do something",
                "unit_amount": 1,
                "project_id": project.id,
                "employee_id": self.env.ref("hr.employee_admin").id,
            }
        )

    def test_analytic_line_parent_project_id(self):
        line_1 = self._create_timesheet(self.iteration_1)
        self.assertEqual(line_1.parent_project_id, self.project_1)
        line_2 = self._create_timesheet(self.project_2)
        self.assertEqual(line_2.parent_project_id, self.project_2)

    def test_block_setting_parent_on_project_with_timesheet(self):
        self._create_timesheet(self.project_1)
        with pytest.raises(ValidationError):
            self.project_1.parent_id = self.project_2

    def test_allow_setting_project_with_timesheet_as_parent(self):
        self._create_timesheet(self.project_1)
        self.project_2.parent_id = self.project_1

    def test_allow_setting_project_without_timesheet_as_parent(self):
        self.project_2.parent_id = self.project_1
