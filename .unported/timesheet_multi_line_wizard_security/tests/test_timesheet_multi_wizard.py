# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.addons.timesheet_multi_line_wizard.tests.common import TimesheetMultiLineCase
from odoo.exceptions import AccessError


class TestTimesheetMultiLine(TimesheetMultiLineCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['extended.security.rule'].search([]).unlink()
        cls.access_line = cls.env['extended.security.rule'].create({
            'model_id': cls.env.ref('analytic.model_account_analytic_line').id,
            'perm_create': True,
        })

    def test_if_not_autorized__raise_error(self):
        with pytest.raises(AccessError):
            self.wizard.action_save()

    def test_if_autorized__error_not_raised(self):
        self.access_line.group_ids = self.env.ref('base.group_user')
        self.wizard.action_save()
