# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HrTimesheetDescriptionTemplate(models.Model):

    _name = "timesheet.description.template"
    _description = "Timesheet Description Template"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    @api.model
    def get_suggestions(self, term):
        lines = self._search_suggestions(term)
        return sorted(lines.mapped("name"))

    def _search_suggestions(self, term):
        return self.search([("name", "ilike", f"%{term}%")])
