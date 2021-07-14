# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from freezegun import freeze_time
from datetime import datetime, timedelta
from odoo.exceptions import AccessError
from odoo.tests import common


class TestAnalyticLineAccess(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager_group = cls.env.ref('hr_timesheet.group_timesheet_manager')

        cls.user = cls.env.ref('base.user_demo')
        cls.user.groups_id -= cls.manager_group
        cls.user.tz = "UTC"

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

        cls.now = datetime(2020, 1, 1)
        cls.today = cls.now.date()
        cls.yesterday = cls.today - timedelta(1)
        cls.tomorrow = cls.today + timedelta(1)

    def check_access(self):
        self.line.sudo(self.user).check_extended_security_write()

    def test_if_yesterday__raise_error(self):
        self.line.date = self.yesterday
        with pytest.raises(AccessError), freeze_time(self.now):
            self.check_access()

    def test_if_tomorrow__raise_error(self):
        self.line.date = self.tomorrow
        with pytest.raises(AccessError), freeze_time(self.now):
            self.check_access()

    def test_if_today__error_not_raised(self):
        self.line.date = self.today
        with freeze_time(self.now):
            self.check_access()

    def test_if_timesheet_manager__error_not_raised(self):
        self.user.groups_id |= self.manager_group
        self.line.date = self.yesterday
        with freeze_time(self.now):
            self.check_access()

    def test_today_in_canada_est(self):
        self.user.tz = "EST"
        self.line.date = self.yesterday
        with freeze_time(self.now):
            self.check_access()


class TestCreateAccess(TestAnalyticLineAccess):

    def check_access(self):
        self.line.sudo(self.user).check_extended_security_create()


class TestDeleteAccess(TestAnalyticLineAccess):

    def check_access(self):
        self.line.sudo(self.user).check_extended_security_unlink()
