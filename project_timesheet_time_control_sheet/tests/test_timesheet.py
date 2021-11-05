# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests import common


class TestTimesheet(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.yesterday = datetime.now().date() - timedelta(1)
        cls.user = cls.env["res.users"].create(
            {
                "name": "My User",
                "login": "test",
                "email": "test@test.com",
            }
        )
        cls.project = cls.env["project.project"].create(
            {"name": "My Project"}
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "My Employee", "user_id": cls.user.id}
        )
        cls.sheet = cls.env["hr_timesheet.sheet"].create(
            {
                "employee_id": cls.employee.id,
                "date_from": cls.yesterday,
                "date_to": cls.yesterday,
            }
        )
        cls.line = cls.env["account.analytic.line"].create(
            {
                "employee_id": cls.employee.id,
                "project_id": cls.project.id,
                "unit_amount": 1,
            })

    def test_restart_timer(self):
        wizard = self._new_wizard(self.line)
        assert wizard.date != self.yesterday
        assert wizard.sheet_id != self.sheet

    def _new_wizard(self, line):
        wizard_obj = self.env["hr.timesheet.switch"].with_context(
            active_model=line._name,
            active_id=line.id,
        )
        defaults = wizard_obj.default_get(["date", "sheet_id"])
        return wizard_obj.new(defaults)
