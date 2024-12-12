# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Payroll Preparation To Payslip",
    "version": "1.0.2",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Payroll",
    "summary": "Convert payroll entries into payslips",
    "depends": [
        "payroll_preparation",
        "hr_payroll",
    ],
    "data": [
        "wizard/payroll_preparation_to_payslip.xml",
        "views/hr_payslip.xml",
        "views/payroll_preparation_line.xml",
    ],
    "installable": True,
}
