# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Payroll Preparation To Payslip Analytic",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Payroll",
    "summary": "Analytical account transfer - "
               "Payroll entry to payroll calculation line",
    "depends": [
        "payroll_preparation_to_payslip",
        "hr_payroll_account",
    ],
    "data": [
        'views/payroll_preparation_line.xml',
        'views/hr_payslip.xml',
        'views/hr_salary_rule.xml',
    ],
    "installable": True,
}
