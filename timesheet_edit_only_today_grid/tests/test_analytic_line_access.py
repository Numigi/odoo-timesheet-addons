# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import common


class TestAnalyticLineAccess(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager_group = cls.env.ref('hr_timesheet.group_timesheet_manager')

        cls.user = cls.env.ref('base.user_demo')
        cls.user.groups_id -= cls.manager_group

        cls.project = cls.env['project.project'].create({
            'name': 'Project 2',
            'allow_timesheets': True,
        })

        cls.task = cls.env['project.task'].create({
            'name': 'Task 2',
            'project_id': cls.project.id,
        })

        cls.line = cls.env['account.analytic.line'].create({
            'name': '/',
            'project_id': cls.project.id,
            'user_id': cls.user.id,
        })

        cls.today = datetime.now().date()
        cls.yesterday = cls.today - timedelta(1)
        cls.tomorrow = cls.today + timedelta(1)

    def adjust_grid(self, date):
        row_domain = [('id', '=', self.line.id)]
        column_field = 'date'
        column_value = fields.Date.to_string(date)
        cell_field = 'unit_amount'
        change = 1
        self.env['account.analytic.line'].sudo(self.user).adjust_grid(
            row_domain, column_field, column_value, cell_field, change
        )

    def test_if_yesterday__raise_error(self):
        with pytest.raises(AccessError):
            self.adjust_grid(self.yesterday)

    def test_if_tomorrow__raise_error(self):
        with pytest.raises(AccessError):
            self.adjust_grid(self.tomorrow)

    def test_if_today__error_not_raised(self):
        self.adjust_grid(self.today)

    def test_if_timesheet_manager__error_not_raised(self):
        self.user.groups_id |= self.manager_group
        self.adjust_grid(self.yesterday)
