# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class PayrollPreparationToPayslipCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create({"name": "Company A"})
        cls.journal = cls.env['account.journal'].create({
            'name': 'Test',
            'code': 'TEST',
            'type': 'general',
        })
        cls.env = cls.env(context=dict(
            cls.env.context,
            journal_id=cls.journal.id,
        ))

        cls.payroll_manager = cls.env["res.users"].create(
            {
                "name": "payroll@manager.com",
                "login": "payroll@manager.com",
                "email": "payroll@manager.com",
                "groups_id": [
                    (4, cls.env.ref("payroll_preparation.group_manager").id),
                    (4, cls.env.ref("hr_payroll.group_hr_payroll_manager").id),
                    (4, cls.env.ref("account.group_account_user").id),
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

        cls.structure = cls.env.ref("hr_payroll.structure_base")
        cls.contract = cls.env["hr.contract"].create(
            {
                "name": "Test",
                "employee_id": cls.employee.id,
                "date_start": cls.date_start,
                "wage": 50000,
                "state": "open",
                "struct_id": cls.structure.id,
                "journal_id": cls.journal.id,
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
