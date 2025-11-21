# © Numigi 2025 (tm) and all its contributors
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestAccountAnalyticLineTaskRequired(TransactionCase):
    """
    Tests ensuring that an analytic line cannot be saved when a project
    is selected but no task is provided.
    """

    def setUp(self):
        super().setUp()

        # Create a project
        self.project = self.env['project.project'].create({
            'name': 'Test Project',
        })

        # Create a task linked to the project
        self.task = self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': self.project.id,
        })

        # Create an employee to associate analytic lines with
        self.employee = self.env['hr.employee'].create({
            'name': 'John Doe',
        })

        self.analytic_account = self.env['account.analytic.account'].create(
            {
                'name': 'Test Project Account',
                'company_id': self.env.company.id,
            }
        )

        self.analytic_line = self.env['account.analytic.line'].create(
            {
                'name': 'Test line',
                'account_id': self.analytic_account.id,
                'project_id': self.project.id,
                'task_id': self.task.id,
                'unit_amount': 1.0,
            }
        )

    # -------------------------------------------------------------------------
    # CREATE TESTS
    # -------------------------------------------------------------------------

    def test_create_valid_line(self):
        """Creating a valid analytic line with project + task should pass."""
        line = self.env['account.analytic.line'].create({
            'name': 'Test AAL',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'employee_id': self.employee.id,
            'account_id': self.analytic_account.id,
            'unit_amount': 2.0,
        })
        self.assertTrue(line.id)

    def test_create_missing_task_raises_error(self):
        """Creating an analytic line without a task should raise an error."""
        with self.assertRaises(ValidationError):
            self.env['account.analytic.line'].create({
                'name': 'Invalid AAL',
                'project_id': self.project.id,   # project set
                'account_id': self.analytic_account.id,
                # task_id not set → error expected
                'employee_id': self.employee.id,
                'unit_amount': 1.0,
            })

    def test_create_without_project_allowed(self):
        """Creating an analytic line with no project is allowed."""
        line = self.env['account.analytic.line'].create({
            'name': 'No Project AAL',
            # project_id not set → allowed
            'account_id': self.analytic_account.id,
            'employee_id': self.employee.id,
            'unit_amount': 1.0,
        })
        self.assertTrue(line.id)

    # -------------------------------------------------------------------------
    # WRITE TESTS
    # -------------------------------------------------------------------------

    def test_write_missing_task_raises_error(self):
        """Writing a project on a line without providing a task must raise."""
        line = self.env['account.analytic.line'].create({
            'name': 'Initial AAL',
            'employee_id': self.employee.id,
            'account_id': self.analytic_account.id,
            'unit_amount': 1.0,
        })

        with self.assertRaises(ValidationError):
            line.write({
                'project_id': self.project.id,  # project set
                # task_id not set → error expected
            })

    def test_write_with_project_and_task_ok(self):
        """Updating an analytic line with project + task is allowed."""
        line = self.env['account.analytic.line'].create({
            'name': 'Initial Line',
            'employee_id': self.employee.id,
            'account_id': self.analytic_account.id,
            'unit_amount': 1.0,
        })

        line.write({
            'project_id': self.project.id,
            'task_id': self.task.id,
        })

        self.assertEqual(line.task_id.id, self.task.id)
