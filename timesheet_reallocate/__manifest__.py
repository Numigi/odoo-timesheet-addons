# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Timesheet Reallocate",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Timesheet",
    "depends": [
        "project_timesheet_time_control",
    ],
    "summary": "Automate a movement of the timeline from one project to another.",
    "data": [
        "views/account_analytic_line_views.xml",
        "wizard/hr_timesheet_transfer_views.xml",
    ],
    "installable": True,
}
