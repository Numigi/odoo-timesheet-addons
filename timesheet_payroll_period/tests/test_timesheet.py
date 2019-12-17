# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from datetime import datetime, timedelta
from odoo.exceptions import AccessError
from odoo.tests import common


@ddt
class TestTimesheetPayrollPeriod(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref('base.user_demo')
        cls.company = cls.env['res.company'].create({'name': 'Company A'})
        cls.other_company = cls.env['res.company'].create({'name': 'Company B'})

        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
            'company_id': cls.company.id,
        })
        cls.other_company_project = cls.env['project.project'].create({
            'name': 'My Other Company Project',
            'company_id': cls.other_company.id,
        })

        cls.line = cls.env['account.analytic.line'].create({
            'name': '/',
            'project_id': cls.project.id,
            'user_id': cls.user.id,
            'company_id': cls.company.id,
        })

        cls.today = datetime.now().date()
        cls.period = cls.env['payroll.period'].create({
            'date_from': cls.today,
            'date_to': cls.today + timedelta(13),
            'company_id': cls.company.id,
        })

    @data(0, 1, 12, 13)
    def test_compute_payroll_period(self, delta):
        self.line.date = self.today + timedelta(delta)
        assert self.line.payroll_period_id == self.period

    @data(-1, 14)
    def test_compute_payroll_period__no_period_found(self, delta):
        self.line.date = self.today + timedelta(delta)
        assert not self.line.payroll_period_id

    def test_if_different_company__no_period_found(self):
        self.line.write({
            'date': self.today + timedelta(1),
            'project_id': self.other_company_project.id,
            'company_id': self.other_company.id,
        })
        assert not self.line.payroll_period_id

    @data(
        (-1, False),
        (0, 1),
        (1, 1),
        (6, 1),
        (7, 2),
        (13, 2),
        (14, False),
    )
    @unpack
    def test_payroll_period_week(self, delta, week):
        self.line.date = self.today + timedelta(delta)
        assert self.line.payroll_period_week == week

    def test_on_period_change__lines_recomputed(self):
        new_date = self.today - timedelta(1)
        self.line.date = new_date
        assert not self.line.payroll_period_id

        self.period.date_from = new_date
        assert self.line.payroll_period_id == self.period

    def test_on_period_create__lines_recomputed(self):
        new_date = self.today - timedelta(1)
        self.line.date = new_date
        assert not self.line.payroll_period_id

        new_period = self.period.copy({
            'date_from': new_date,
            'date_to': new_date,
        })
        assert self.line.payroll_period_id == new_period
