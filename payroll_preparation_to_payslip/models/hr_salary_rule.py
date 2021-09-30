# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SalaryRule(models.Model):

    _inherit = "hr.salary.rule"

    @api.multi
    def _compute_rule(self, localdict):
        dict_ = self._get_dict_with_entries(localdict)
        return super()._compute_rule(dict_)

    @api.multi
    def _satisfy_condition(self, localdict):
        dict_ = self._get_dict_with_entries(localdict)
        return super()._satisfy_condition(dict_)

    def _get_dict_with_entries(self, dict_):
        return dict(dict_, entries=_PayrollEntries(self.env, dict_))


class _PayrollEntries:

    def __init__(self, env, localdict):
        self._env = env
        self._localdict = localdict

    def __getattr__(self, code):
        if code.startswith("_"):
            return object.__getattribute__(self, code)

        return self._get_amount(code)

    def _get_amount(self, code):
        entries = self._get_payslip().payroll_entry_ids.filtered(lambda e: e.code == code)
        return sum(e.amount for e in entries)

    def _get_payslip(self):
        payslip_id = self._localdict["payslip"].id
        return self._env["hr.payslip"].browse(payslip_id)
