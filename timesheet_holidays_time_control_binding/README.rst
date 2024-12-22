Timesheet Holidays Time Control Binging
=======================================
This module makes the module `project_timesheet_time_control <https://github.com/OCA/project/tree/12.0/project_timesheet_time_control>`_ compatible with `project_timesheet_holidays`.

It allows to approve leave requests in advance while associating them with the date selected by the employee, rather than saving them on the validation date.

Usage
-----
As Leave Manager,
I validate leave for an employee requested for a later date,
Imputation on timesheets is made for the leave date and not the validation date

.. image:: static/description/leave_validated.png

The leave is charged to timesheets whose date is equivalent to the leave date and not the validation date.

.. image:: static/description/timesheets_from_leave.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
