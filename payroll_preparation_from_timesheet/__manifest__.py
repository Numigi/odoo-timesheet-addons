# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Payroll Preparation From Timesheet',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'summary': 'Import payroll entries from timesheets',
    'depends': [
        'payroll_preparation',
        'timesheet_payroll_period',
    ],
    'data': [
        'wizard/payroll_preparation_from_timesheet.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
