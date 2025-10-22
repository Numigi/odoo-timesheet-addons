# Copyright Numigi 2025 (tm) and all its contributors
# (https://numigi.com/r/home)
# License LGPL-3.0 or later
# (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Timesheet Confirm Reset',
    'version': '14.0.1.0.0',
    'summary': 'Allow user to reset submitted timesheet to draft',
    'description': """
This module implements:
- A confirmation message when a user clicks 'Submit to Manager'
  to avoid accidental submissions.
- A button for the timesheet owner to reset their submitted
  timesheet back to Draft, as long as it has NOT been approved.
""",
    'category': 'Human Resources',
    'author': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_timesheet_sheet',
    ],
    'data': [
        'views/hr_timesheet_sheet_sheet.xml',
    ],
    'installable': True,
    'application': False,
}
