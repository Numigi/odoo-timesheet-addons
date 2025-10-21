# Copyright Numigi 2025 (tm) and all its contributors
# (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestHrTimesheetSheetConfirmReset(TransactionCase):

    def setUp(self):
        super(TestHrTimesheetSheetConfirmReset, self).setUp()
        # Create a test employee user
        self.employee_user = self.env['res.users'].create(
            {'name': 'Test Employee', 'login': 'employee_test', })

        # Assign hr_timesheet_user group
        group = self.env.ref('hr_timesheet.group_hr_timesheet_user')
        group.users = [(4, self.employee_user.id)]

        # Create employee linked to the user
        self.employee = self.env['hr.employee'].create(
            {'name': 'Test Employee', 'user_id': self.employee_user.id, })

        # Create a timesheet sheet in 'confirm' state
        self.timesheet = self.env['hr_timesheet.sheet'].sudo().create(
            {'name': 'Test Timesheet', 'user_id': self.employee_user.id,
                'employee_id': self.employee.id, 'state': 'confirm', })
