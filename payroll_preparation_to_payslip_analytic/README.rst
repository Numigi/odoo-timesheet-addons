Payroll Preparation To Payslip Analytics
========================================

.. contents:: Table of Contents

Overview
--------
This module allows to:
- Systematically propagate the analytical account of payroll entries on the calculation lines of the payslip,
- Add a condition on the generation of accounting entries for the propagation of the analytical account from `Salary Computation Lines` to `Journal Item Lines`,

Usage
-----

Generate The Payslip
~~~~~~~~~~~~~~~~~~~~
As member of the groups `Payroll Preparation / User` and `Payroll / Manager`,

- I go to the form view of payroll entries, I see that the `Analytic Account` field has become mandatory:

- I go to the list view of payroll entries, I select a set of entries witch have the same analytic account and I click on `Generate Payslips`.
    .. image:: static/description/payroll_entries_generate_payslip.png

- I see that the analytic account is propagated on the Payslip and its calculation lines:
    .. image:: static/description/analytic_account_propagation_to_payslip.png


Uniqueness Constraint
~~~~~~~~~~~~~~~~~~~~~
- When I select a set of entries witch have different analytic accounts
  and I click on `Generate Payslips`, a blocking message is displayed.

.. image:: static/description/uniqueness_constraint_to_generate_payslip.png


Configuration
~~~~~~~~~~~~~
As member of the groups `Payroll / Manager`,
I go to the form view of a `Salary Rule`, Tab `Accounting`.
I see that the Analytic Account field is no longer displayed, and two checkboxes fields are added:
- Propagate Payroll Entries Analytic Account (Debit)
- Propagate Payroll Entries Analytic Account (Credit)

.. image:: static/description/salary_rule_accounting_configuration.png

I check `Propagate Payroll Entries Analytic Account (Credit)` for `Net Salary`
and `Propagate Payroll Entries Analytic Account (Debit)` for `Gross`

.. image:: static/description/salary_rule_1_config.png

.. image:: static/description/salary_rule_2_config.png

I go to my payslip witch has the 2 salary rules in `Salary Computation Lines`,
then I confirm the Payslip.

.. image:: static/description/confirmed_payslip.png

I go to `Accounting Information Tab / Accounting Entry`
to display the `Accounting Entry` generated after confirming the payslip.

.. image:: static/description/accounting_entry_generated.png

I can see that the `Analytic Account` has propagated on the lines of the `Accounting Entry`.

.. image:: static/description/accounting_entry_lines_analytic_account.png


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)


More information
----------------
* Meet us at https://bit.ly/numigi-com
