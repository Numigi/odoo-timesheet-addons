# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class Timesheet(models.Model):

    _inherit = "hr_timesheet.sheet"

    def action_timesheet_confirm(self):
        for line in self.timesheet_ids:
            if not line.unit_amount:
                raise ValidationError(
                    _(
                        "The timesheet can not be submitted because the "
                        "timesheet line {} has an open timer."
                    ).format(line.display_name)
                )
        super().action_timesheet_confirm()
