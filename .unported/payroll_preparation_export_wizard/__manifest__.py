# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Payroll Preparation Export Wizard',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'summary': 'Export payroll entries into a file',
    'depends': [
        'payroll_preparation',
    ],
    'data': [
        'wizard/payroll_preparation_export.xml',
        'views/payroll_preparation_export_history.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': True,
}
