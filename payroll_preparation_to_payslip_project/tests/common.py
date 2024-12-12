# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationToPayslipCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env["res.company"].create({"name": "Company A"})

        cls.payroll_manager = cls.env["res.users"].create(
            {
                "name": "payroll@manager.com",
                "login": "payroll@manager.com",
                "email": "payroll@manager.com",
                "groups_id": [
                    (4, cls.env.ref("payroll_preparation.group_manager").id),
                    (4, cls.env.ref("hr_payroll.group_hr_payroll_manager").id),
                ],
                "company_id": cls.company.id,
                "company_ids": [(4, cls.company.id)],
            }
        )

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "John Doe",
                "company_id": cls.company.id,
            }
        )

        cls.date_start = datetime.now().date()
        cls.date_end = cls.date_start + timedelta(30)

        cls.entry_1 = cls._create_entry(cls.date_start)
        cls.entry_2 = cls._create_entry(cls.date_end)

        cls.analytic_1 = cls.env["account.analytic.account"].create(
            {"name": "Analytic 1"}
        )
        cls.analytic_2 = cls.env["account.analytic.account"].create(
            {"name": "Analytic 2"}
        )
        cls.project_1 = cls.env["project.project"].create(
            {"name": "Project 1"}
        )
        cls.project_2 = cls.env["project.project"].create(
            {"name": "Project 2"}
        )

        cls.account_debit = cls.env["account.account"].create({
            "name": "Account Debit",
            "code": 210110,
            'user_type_id': cls.env.ref(
                'account.data_account_type_payable').id,
            'reconcile': True,
        })

        cls.account_credit = cls.env["account.account"].create({
            "name": "Account Credit",
            "code": 510110,
            'user_type_id': cls.env.ref(
                'account.data_account_type_expenses').id,
            'reconcile': True,
        })

        cls.structure = cls.env.ref("hr_payroll.structure_base")
        cls.contract = cls.env["hr.contract"].create(
            {
                "name": "Test",
                "employee_id": cls.employee.id,
                "date_start": cls.date_start,
                "wage": 50000,
                "state": "open",
                "struct_id": cls.structure.id,
            }
        )

    @classmethod
    def _create_entry(cls, date_):
        return cls.env["payroll.preparation.line"].create(
            {
                "date": date_,
                "employee_id": cls.employee.id,
                "company_id": cls.company.id,
            }
        )
