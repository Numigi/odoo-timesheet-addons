# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytz
from datetime import datetime, time
from odoo import _, api, fields, models


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'
    _order = 'date_time desc'

    @api.model
    def create(self, vals):
        line = super().create(vals)

        if vals.get("date") and not vals.get("date_time"):
            line.date_time = line._get_datetime_from_date()

        return line

    def write(self, vals):
        super().write(vals)

        if self and vals.get("date") and not vals.get("date_time"):
            self.write({'date_time': self[0]._get_datetime_from_date()})

        return True

    def _get_datetime_from_date(self):
        naive_timestamp = datetime.combine(self.date, time.min)

        tz_name = self._context.get('tz') or self.env.user.tz or 'UTC'
        tz = pytz.timezone(tz_name)
        tz_timestamp = tz.localize(naive_timestamp)

        utc_datetime = tz_timestamp.astimezone(pytz.utc)
        return fields.Datetime.to_string(utc_datetime)
