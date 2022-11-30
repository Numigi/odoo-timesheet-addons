# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Payroll Preparation',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Payroll',
    'summary': 'Preparation of data for the payroll',
    'depends': [
        'analytic',
        'mail',
        'hr',
        'payroll_period',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/payroll_preparation_line.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
