# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Timesheet filter closed task",
    "version": "12.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Timesheets",
    "summary": """Ensures that only open tasks are
    displayed when recording timesheets.""",
    "depends": [
        "hr_timesheet",
        "project_stage_closed",
        "project_task_stage_allow_timesheet"
    ],
    "installable": True
}
