# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestSuggestions(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["timesheet.description.template"].search([]).write({"active": False})

    @classmethod
    def _create_template(cls, term):
        return cls.env["timesheet.description.template"].create({
            "name": term,
        })

    @classmethod
    def _get_suggestions(cls, term):
        return cls.env["timesheet.description.template"].get_suggestions(term)

    def test_suggestions(self):
        template = self._create_template("Hello World")
        assert self._get_suggestions("Hello")
        assert self._get_suggestions("world")
