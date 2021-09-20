# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Payroll Preparation From Project",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Payroll",
    "summary": "Generate payroll entries from projects",
    "depends": [
        "payroll_preparation",
        "project",
    ],
    "data": [
        "wizard/payroll_preparation_from_project.xml",
        "views/project.xml",
        "views/payroll_preparation_line.xml",
    ],
    "installable": True,
}
