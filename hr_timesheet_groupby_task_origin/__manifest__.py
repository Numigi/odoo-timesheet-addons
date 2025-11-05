# Copyright Numigi 2025 (tm) and all its contributors
# (https://numigi.com/r/home)
# License LGPL-3.0 or later
# (http://www.gnu.org/licenses/lgpl).

{
    'name': 'HR Timesheet Group by Task Origin',
    'version': '14.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Group timesheet lines by origin task instead of current task',
    'description': """
        HR Timesheet Group by Task Origin
        =================================

        This module fixes the inconsistent task grouping behavior between
        Accounting and Project applications for analytic lines.

        Issue:
        --------
        - In Accounting app, task grouping uses origin_task_id field
        - In Project app (Costs/Revenues), task grouping uses task_id field
        - This causes inconsistent grouping results between the two apps

        Solution:
        ---------
        - Modifies the task grouping in Project app's Costs/Revenues view to
          use origin_task_id instead of task_id
        - Aligns the grouping behavior with Accounting app
        - Ensures consistent analytic reporting across applications
    """,
    'author': 'Numigi',
    'website': 'https://www.numigi.com',
    'depends': [
        'hr_timesheet',
        'project'
    ],
    'data': [
        'views/hr_timesheet_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
