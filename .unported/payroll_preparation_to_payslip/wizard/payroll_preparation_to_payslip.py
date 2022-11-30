# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollPreparationToPayslip(models.TransientModel):

    _name = "payroll.preparation.to.payslip"
    _description = "Payroll Preparation To Payslip"

    entry_ids = fields.Many2many(
        "payroll.preparation.line",
        "payroll_preparation_to_payslip_entry_rel",
        "wizard_id",
        "entry_id",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_ids = self._context.get("active_ids") or []
        res["entry_ids"] = [(6, 0, active_ids)]

        return res

    def action_validate(self):
        self._check_entry_dates()
        self._check_entry_with_payslip()
        self._generate_payslips()
        return self._get_payslip_list_action()

    def _check_entry_dates(self):
        for entry in self.entry_ids:
            if not entry.date:
                raise ValidationError(
                    _(
                        "In order to generate the payslips, "
                        "all selected payroll entries must have a date.\n"
                        "The entry {} has no date."
                    ).format(entry.display_name)
                )

    def _check_entry_with_payslip(self):
        for entry in self.entry_ids:
            if entry.payslip_id:
                raise ValidationError(
                    _(
                        "A payroll entry can not be used twice to generate a payslip.\n"
                        "The entry {entry} is already linked to the payslip {payslip}."
                    ).format(
                        entry=entry.display_name, payslip=entry.payslip_id.display_name
                    )
                )

    def _generate_payslips(self):
        payslips = self._create_payslips()
        self._compute_payslips(payslips)

    def _create_payslips(self):
        payslips = self.env["hr.payslip"]

        errors = []

        for entries in self._group_entries():
            try:
                payslip = self._create_payslip(entries)
            except ValidationError as err:
                errors.append(err)
            else:
                entries.write({"payslip_id": payslip.id})
                payslips |= payslip

        if errors:
            raise ValidationError(
                "\n\n".join(err.name for err in errors)
            )

        return payslips

    def _compute_payslips(self, payslips):
        payslips.compute_sheet()

    def _group_entries(self):
        res = {}

        for entry in self.entry_ids:
            key = self._get_grouping_key(entry)

            if key not in res:
                res[key] = entry
            else:
                res[key] |= entry

        return res.values()

    def _get_grouping_key(self, entry):
        return (entry.employee_id.id, entry.company_id.id)

    def _create_payslip(self, entries):
        vals = self._get_payslip_vals(entries)
        payslip = self.env["hr.payslip"].create(vals)
        payslip.onchange_employee()

        if not payslip.contract_id:
            raise ValidationError(
                _(
                    "The payslip of {employee} could not be generated. "
                    "The employee seems to have no active contract for "
                    "the given period ({date_from} to {date_to})."
                ).format(
                    employee=payslip.employee_id.display_name,
                    date_from=payslip.date_from,
                    date_to=payslip.date_to,
                )
            )

        if not payslip.struct_id:
            raise ValidationError(
                _(
                    "The payslip of {employee} could not be generated. "
                    "The employee's contract ({contract}) seems to have no "
                    "payroll structure."
                ).format(
                    employee=payslip.employee_id.display_name,
                    contract=payslip.contract_id.display_name,
                )
            )

        return payslip

    def _get_payslip_vals(self, entries):
        employee = entries[0].employee_id
        company = entries[0].company_id
        return {
            "date_from": min(e.date for e in entries),
            "date_to": max(e.date for e in entries),
            "employee_id": employee.id,
            "company_id": company.id,
        }

    def _get_payslip_list_action(self):
        action = self.env.ref("hr_payroll.action_view_hr_payslip_form").read()[0]
        action["domain"] = [("id", "in", self.mapped("entry_ids.payslip_id.id"))]
        return action
