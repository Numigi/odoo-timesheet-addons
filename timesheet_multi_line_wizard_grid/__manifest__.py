# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Timesheet Multi Line Wizard / Grid',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Timesheet',
    'summary': 'Open the timesheet multi-line wizard from the grid view',
    'depends': [
        'timesheet_multi_line_wizard',
        'timesheet_grid',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
