Timesheet Holidays Time Control Compatible
==========================================
This module makes the module `project_timesheet_time_control <https://github.com/OCA/project/tree/16.0/project_timesheet_time_control>`_ compatible with `project_timesheet_holidays`.

This module allows to approve leave requests in advance while associating them with the date selected by the employee, rather than saving them on the validation date.

Usage
-----
As Leave Manager,
- I validate leave for an employee requested for a later date,
- Imputation on timesheets is made for the leave date and not the validation date

.. image:: https://raw.githubusercontent.com/Numigi/odoo-timesheet-addons/16.0/timesheet_holidays_time_control_compatible/static/description/leave_validated.png

The leave is charged to timesheets whose date is equivalent to the leave date and not the validation date.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-timesheet-addons/16.0/timesheet_holidays_time_control_compatible/static/description/timesheets_from_leave.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
