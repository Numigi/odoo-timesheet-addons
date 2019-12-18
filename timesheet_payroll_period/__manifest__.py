# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Timesheet Payroll Periods',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Timesheet',
    'summary': 'Add payroll periods',
    'depends': [
        'hr_timesheet',
        'payroll_period',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_line.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
