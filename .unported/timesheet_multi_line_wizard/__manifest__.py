# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Timesheet Multi Line Wizard',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Timesheet',
    'summary': 'Add a wizard for filling timesheets faster.',
    'depends': [
        'hr_timesheet',
    ],
    'data': [
        'wizard/timesheet_multi_wizard.xml',
    ],
    'installable': True,
}
