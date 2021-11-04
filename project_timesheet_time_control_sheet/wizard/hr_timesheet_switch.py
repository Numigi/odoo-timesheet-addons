# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class HrTimesheetSwitch(models.TransientModel):

    _inherit = "hr.timesheet.switch"

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)

        if "sheet_id" in result:
            result["sheet_id"] = False

        return result
