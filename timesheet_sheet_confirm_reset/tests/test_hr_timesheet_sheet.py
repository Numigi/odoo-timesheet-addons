# © Numigi 2025 (tm) and all its contributors
# (https://numigi.com/r/home)
# License LGPL-3.0 or later
# (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestHrTimesheetSheetConfirmReset(TransactionCase):

    def setUp(self):
        super().setUp()

        # Create employee user
        self.employee_user = self.env['res.users'].create({
            'name': 'Test Employee',
            'login': 'employee_test',
        })

        # Assign hr_timesheet_user group
        group = self.env.ref('hr_timesheet.group_hr_timesheet_user')
        group.users = [(4, self.employee_user.id)]

        # Create employee linked to user
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'user_id': self.employee_user.id,
        })

        # Create reviewer user
        self.reviewer_user = self.env['res.users'].create({
            'name': 'Reviewer',
            'login': 'reviewer_test',
        })

        # Assign timesheet approver group
        reviewer_group = self.env.ref(
            'hr_timesheet.group_hr_timesheet_approver'
        )
        reviewer_group.users = [(4, self.reviewer_user.id)]

        # Create reviewer employee
        self.reviewer = self.env['hr.employee'].create({
            'name': 'Reviewer',
            'user_id': self.reviewer_user.id,
        })

        # Create timesheet in 'confirm' state with reviewer
        self.timesheet = self.env['hr_timesheet.sheet'].sudo().create({
            'name': 'Test Timesheet',
            'employee_id': self.employee.id,
            'reviewer_id': self.reviewer.id,
            'state': 'draft',
        })

    def test_reset_to_draft_success(self):
        """Employee resets their own submitted sheet to draft."""
        self.timesheet = self.timesheet.with_user(self.employee_user)
        # Submit the sheet
        self.timesheet.action_timesheet_confirm()
        # Reset to draft
        result = self.timesheet.action_confirm_reset()
        # Should return True
        self.assertTrue(result)
        self.assertEqual(self.timesheet.state, 'draft')

    def test_reset_to_draft_approved_error(self):
        """Resetting an approved timesheet raises an error."""
        # Approve the sheet
        self.timesheet.reviewer_id = self.reviewer.id
        self.timesheet = self.timesheet.with_user(self.reviewer_user)
        self.timesheet.action_timesheet_confirm()
        self.timesheet.action_timesheet_done()
        # Employee tries to reset approved sheet
        self.timesheet = self.timesheet.with_user(self.employee_user)
        with self.assertRaises(UserError) as e:
            self.timesheet.action_confirm_reset()
        self.assertIn(
            'You cannot reset a timesheet that has already been approved',
            str(e.exception)
        )
