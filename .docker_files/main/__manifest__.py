# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'payroll_code_on_task_type',
        'payroll_period',
        'payroll_preparation',
        'payroll_preparation_from_timesheet',
        'timesheet_edit_only_today',
        'timesheet_list_description_after_task',
        'timesheet_list_employee',
        'timesheet_multi_line_wizard',
        'timesheet_multi_line_wizard_grid',
        'timesheet_multi_line_wizard_security',
        'timesheet_payroll_period',
        'timesheet_validation_status',
        'timesheet_validation_status_enterprise',
    ],
    'installable': True,
}
