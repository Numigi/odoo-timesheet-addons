# Copyright Numigi 2025 2025 (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestHrTimesheetSheetConfirmReset(TransactionCase):

    def setUp(self):
        super(TestHrTimesheetSheetConfirmReset, self).setUp()
        # Create a test employee user
        self.employee_user = self.env['res.users'].create({
            'name': 'Test Employee',
            'login': 'employee_test',
        })

        # Assign hr_timesheet_user group
        group = self.env.ref('hr_timesheet.group_hr_timesheet_user')
        group.users = [(4, self.employee_user.id)]

        # Create a timesheet sheet in 'confirm' state
        self.timesheet = self.env['hr_timesheet.sheet'].sudo().create({
            'name': 'Test Timesheet',
            'user_id': self.employee_user.id,
            'state': 'confirm',
        })

    def test_reset_to_draft_success(self):
        """Employee resets their own submitted sheet to draft"""
        self.timesheet = self.timesheet.with_user(self.employee_user)
        result = self.timesheet.action_confirm_reset()
        self.assertTrue(result)
        self.assertEqual(self.timesheet.state, 'draft')

    def test_reset_to_draft_approved_error(self):
        """Resetting an already approved timesheet raises an error"""
        # Set timesheet state to 'done' (approved)
        self.timesheet.sudo().write({'state': 'done'})
        self.timesheet = self.timesheet.with_user(self.employee_user)
        with self.assertRaises(UserError) as e:
            self.timesheet.action_confirm_reset()
        self.assertIn('Error: You cannot reset a timesheet that has already been approved', str(e.exception))
