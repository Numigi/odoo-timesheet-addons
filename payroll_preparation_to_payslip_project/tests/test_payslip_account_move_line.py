# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import PayrollPreparationToPayslipCase


class TestPayslip(PayrollPreparationToPayslipCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.amount_1 = 100
        cls.entry_1.amount = cls.amount_1
        cls.entry_1.code = "AAA"

        cls.payslip = cls.env["hr.payslip"].create(
            {
                "employee_id": cls.employee.id,
                "company_id": cls.company.id,
                "contract_id": cls.contract.id,
                "struct_id": cls.structure.id,
                "date_from": cls.date_start,
                "date_to": cls.date_end,
                "credit_note": True,
                "project_id": cls.project_1.id,
            }
        )
        cls.payslip.payroll_entry_ids = cls.entry_1 | cls.entry_2
        cls.rule = cls.env.ref("hr_payroll.hr_rule_basic")
        cls.rule.write(
            {
                "amount_select": "code",
                "amount_python_compute": "result = entries.AAA",
            }
        )
        cls.structure.rule_ids[0].write({
            'account_debit': cls.account_debit.id,
            'propagate_account_debit': True,
        })
        cls.structure.rule_ids[1].write({
            'account_credit': cls.account_credit.id,
            'propagate_account_credit': True,
        })

    def test_move_lines_project_application(self):
        """Check the correct conditioning on the application of the analytical
         account in the lines of accounting entries from the payslip lines"""
        self.payslip.compute_sheet()
        self.payslip.action_payslip_done()
        move_lines_project = \
            self.payslip.move_id.line_ids.mapped('project_id')
        assert len(move_lines_project) == 1 and \
               self.project_1 in move_lines_project
