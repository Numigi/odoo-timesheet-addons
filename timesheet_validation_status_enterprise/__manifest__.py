# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Timesheet Validation Status / Enterprise",
    "version": "1.0.0",
    "category": "Timesheets",
    "author": "Numigi",
    "license": "LGPL-3",
    "summary": "Timesheet validation for Odoo Enterprise",
    "depends": [
        "timesheet_grid",
        "timesheet_validation_status",
    ],
    "data": [
        "views/account_analytic_line.xml",
        "views/hr_employee.xml",
    ],
    "installable": True,
}
