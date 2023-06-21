# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Payroll Preparation To Payslip Project",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Payroll",
    "summary": "Project transfer - "
               "Payroll entry to payroll calculation line",
    "depends": [
        "hr_payroll_account",
        "payroll_preparation_to_payslip",
        "project",
    ],
    "data": [
        'views/hr_payslip.xml',
    ],
    "installable": True,
}
