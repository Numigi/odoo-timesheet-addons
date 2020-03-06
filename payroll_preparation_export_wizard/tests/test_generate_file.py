# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from .common import PayrollPreparationExportCase
from ..wizard.payroll_preparation_export import (
    DEFAULT_FILE_NAME,
    DEFAULT_FILE_CONTENT,
)


class TestPayrollPreparationExport(PayrollPreparationExportCase):

    def test_get_payroll_preparation_lines(self):
        self.create_payroll_entry(self.period_1)
        line_2 = self.create_payroll_entry(self.period_2)
        line_3 = self.create_payroll_entry(self.period_2)
        wizard = self.open_wizard(self.period_2)
        assert wizard.get_payroll_preparation_lines() == line_2 | line_3

    def test_on_validate__one_history_entry_created(self):
        wizard = self.open_wizard(self.period_2)
        wizard.action_validate()
        entry = self.find_history_entry(self.period_2)
        assert len(entry) == 1

    def test_user_propagated_to_history_entry(self):
        wizard = self.open_wizard(self.period_2)
        wizard.action_validate()
        entry = self.find_history_entry(self.period_2)
        assert entry.user_id == self.payroll_manager

    def test_file_generated(self):
        wizard = self.open_wizard(self.period_2)
        wizard.action_validate()
        entry = self.find_history_entry(self.period_2)
        assert entry.filename == DEFAULT_FILE_NAME

        content = base64.b64decode(entry.file).decode('utf-8')
        assert content == DEFAULT_FILE_CONTENT
