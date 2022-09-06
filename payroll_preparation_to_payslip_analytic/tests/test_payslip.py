# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
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
                "analytic_account_id": cls.analytic_1.id,
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

    def test_payslip_lines_account_analytic_application(self):
        """ Check the systematic application of the analytical account
        on the payslip calculation lines"""
        self.payslip.compute_sheet()
        line_analytic_accounts = \
            self.payslip.line_ids.mapped('analytic_account_id')
        assert len(line_analytic_accounts) == 1 and \
               self.analytic_1 in line_analytic_accounts

    def test_move_lines_account_analytic_application(self):
        """Check the correct conditioning on the application of the analytical
         account in the lines of accounting entries from the payslip lines"""
        self.payslip.compute_sheet()
        self.payslip.action_payslip_done()
        move_lines_analytic_accounts = \
            self.payslip.move_id.line_ids.mapped('analytic_account_id')
        assert len(move_lines_analytic_accounts) == 1 and \
               self.analytic_1 in move_lines_analytic_accounts

    def _get_rule_form_view_arch(self):
        view = self.env.ref("hr_payroll.hr_salary_rule_form")
        arch = self.env["hr.salary.rule"].fields_view_get(
            view_id=view.id)["arch"]
        return etree.fromstring(arch)

    def test_analytic_account_id_visibility_in_rule_form_view(self):
        """Verify that the analytic_account_id field cannot
        be populated in payroll rules"""

        form_view = self._get_rule_form_view_arch()
        el = form_view.xpath("//field[@name='analytic_account_id']")[0]
        assert el.attrib["invisible"] == '1'
