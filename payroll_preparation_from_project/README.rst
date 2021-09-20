Payroll Preparation From Project
================================

.. contents:: Table of Contents

Overview
--------
This module allows to generate payroll entries from a project.

When only this module is installed, no payroll entries are generated.

However, another module can implement how the preparation lines are created for a given project.

Usage
-----
In the form view of a project, a new action button is added.

.. image:: static/description/project_action_menu.png

When clicking on this button, a wizard is open.

.. image:: static/description/wizard.png

The wizard allows to select a payroll period.

.. image:: static/description/wizard_filled.png

After clicking on ``Validate``, payroll entries are created for this project.

.. image:: static/description/payroll_entry_list.png

Project Smart Button
--------------------
The module also adds a smart button in the form view of a project.

.. image:: static/description/project_smart_button.png

When I click on the button, I see the list payroll entries generated from this project.

.. image:: static/description/payroll_entry_list.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
