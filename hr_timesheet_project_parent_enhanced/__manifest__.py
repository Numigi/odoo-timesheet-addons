# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Hr Timesheet Project Parent Enhanced",
    "version": "16.0.1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": """
        Adds constraints and features related to timesheets
        and parent-child relationships between projects.
    """,
    "depends": ["hr_timesheet", "project_parent_enhanced"],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
}
