# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tests import common


class TestTimesheet(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.yesterday = datetime.now() - timedelta(1)
        cls.user = cls.env["res.users"].create(
            {
                "name": "My User",
                "login": "test",
                "email": "test@test.com",
            }
        )
        cls.project = cls.env["project.project"].create({"name": "My Project"})
        cls.employee = cls.env["hr.employee"].create(
            {"name": "My Employee", "user_id": cls.user.id}
        )
        cls.sheet = cls.env["hr_timesheet.sheet"].create(
            {
                "employee_id": cls.employee.id,
                "date_from": cls.yesterday.date(),
                "date_to": cls.yesterday.date(),
            }
        )
        cls.line = cls.env["account.analytic.line"].create(
            {
                "employee_id": cls.employee.id,
                "project_id": cls.project.id,
                "unit_amount": 1,
                "sheet_id": cls.sheet.id,
                "date": cls.yesterday.date(),
                "date_time": cls.yesterday,
            }
        )

    def test_sheet_not_propagated_to_new_line(self):
        wizard = self._new_wizard(self.line)
        assert wizard.date != self.yesterday
        assert wizard.sheet_id != self.sheet

    def test_delete_submitted_timesheet_with_open_timer(self):
        self.line.unit_amount = 0
        self.sheet.state = "confirm"
        self.line.unlink()
        assert not self.line.exists()

    def test_delete_submitted_timesheet_with_closed_timer(self):
        self.sheet.state = "confirm"
        self.line.sheet_id = self.sheet.id
        with pytest.raises(UserError):
            self.line.unlink()

    def test_submit_timesheet_with_open_timer(self):
        self.line.unit_amount = 0
        self.line.sheet_id = self.sheet.id
        with pytest.raises(ValidationError):
            self.sheet.action_timesheet_confirm()

    def test_submit_timesheet_with_no_open_timer(self):
        self.sheet.action_timesheet_confirm()
        assert self.sheet.state == "confirm"

    def _new_wizard(self, line):
        wizard_obj = self.env["hr.timesheet.switch"].with_context(
            active_model=line._name,
            active_id=line.id,
        )
        defaults = wizard_obj.default_get(["date", "sheet_id"])
        return wizard_obj.new(defaults)
