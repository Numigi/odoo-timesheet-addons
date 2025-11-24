Timesheet Project Task Validation
=================================

This module ensures consistency between projects and tasks in timesheets.

Description
-----------

This module adds validation logic to the Timesheet and Analytic Line models to prevent data inconsistency:

1.  **Consistency**: It ensures that a Task is always selected when a Project is set.
2.  **Validation**: It prevents saving timesheet lines if the Task is missing.
3.  **UI Behavior**: It automatically clears the Task field when the Project is changed in the "Summary" tab of the Timesheet Sheet to force a correct selection.

Usage
-----

As a user filling out a Timesheet:

**1. Automatic Task Clearing (Summary Tab)**

When I change the **Project** on a timesheet line in the "Summary" tab, the **Task** field is automatically cleared.

.. image:: static/description/project_change_clear_task.png

This mechanism prevents the accidental association of a task from a previous project to a newly selected project.

**2. Validation when Adding a Line**

In the "Summary" tab, if I select a Project but attempt to click "Add a line" without selecting a **Task**, the system blocks the action and displays the following error message:

* *"Please fill in the 'Task' field before adding a line."*

.. image:: static/description/error_add_line_no_task.png

**3. Validation when Saving (Details Tab & Global)**

If I attempt to save a timesheet line (Analytic Line) in the "Details" tab or any other view where the **Project** is set but the **Task** is empty, the system blocks the save and displays the following error message:

* *"Please fill in the 'Task' field before saving."*

.. image:: static/description/error_save_no_task.png

Contributors
------------

* The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.