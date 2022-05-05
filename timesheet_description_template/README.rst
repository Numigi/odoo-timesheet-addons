Timesheet Description Templates
===============================
This module allows to autocomplete timesheet descriptions.

.. contents:: Table of Contents

Usage
-----
As ``Timesheet / Manager``, I go to ``Timesheets / Configuration / Description Templates``.

.. image:: static/description/description_template_list.png

I create a few records.

.. image:: static/description/description_template_list_filled.png

I go to the list view of timesheet entries.

.. image:: static/description/timesheet_list.png

As I begin typing the description, suggestions are proposed.

.. image:: static/description/timesheet_suggestions.png

I can select one of these suggestions.

.. image:: static/description/timesheet_suggestion_selected.png

Then, I can manually customize the description for this timesheet entry.

.. image:: static/description/timesheet_suggestion_customized.png

Using the Widget
----------------
The autocomplete widget (``timesheet_description_autocomplete``) is added by default on the most common views of timesheets.

It can be added in other views (even other models than timesheets).
The only requirement is that the field must be a ``Char`` field.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
